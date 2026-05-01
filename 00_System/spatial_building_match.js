/**
 * SPATIAL MATCHING - OS-PALANTHAI
 * Matches project coordinates to building footprints using turf.js
 */

import * as turf from '@turf/turf';

/**
 * Find which building footprint contains a given point (lat/lng)
 * Uses turf.booleanPointInPolygon for precise point-in-polygon testing
 *
 * @param {number} lng - Longitude of the project
 * @param {number} lat - Latitude of the project
 * @param {Array} buildingsGeoJson - GeoJSON FeatureCollection of building polygons
 * @returns {Object|null} The matching building feature or null
 */
export function findBuildingForPoint(lng, lat, buildingsGeoJson) {
  if (!buildingsGeoJson?.features?.length) return null;

  const point = turf.point([lng, lat]);

  for (const feature of buildingsGeoJson.features) {
    if (feature.geometry?.type === 'Polygon') {
      const polygon = turf.polygon(feature.geometry.coordinates);
      if (turf.booleanPointInPolygon(point, polygon)) {
        return feature;
      }
    }
  }

  return null;
}

/**
 * Find closest building footprint to a point (fallback when no exact match)
 * Uses turf.pointToLineDistance for proximity search
 *
 * @param {number} lng - Longitude
 * @param {number} lat - Latitude
 * @param {Array} buildingsGeoJson - GeoJSON FeatureCollection
 * @param {number} maxDistanceMeters - Maximum search radius
 * @returns {Object|null} The closest building or null
 */
export function findClosestBuilding(lng, lat, buildingsGeoJson, maxDistanceMeters = 100) {
  if (!buildingsGeoJson?.features?.length) return null;

  const point = turf.point([lng, lat]);
  let closest = null;
  let minDistance = Infinity;

  for (const feature of buildingsGeoJson.features) {
    if (feature.geometry?.type === 'Polygon') {
      const polygon = turf.polygon(feature.geometry.coordinates);
      const centroid = turf.centroid(polygon);
      const distance = turf.distance(point, centroid, { units: 'meters' });

      if (distance < minDistance && distance <= maxDistanceMeters) {
        minDistance = distance;
        closest = feature;
      }
    }
  }

  return closest;
}

/**
 * Match all projects to their building footprints
 * Returns projects with matched building data attached
 *
 * @param {Array} projects - Array of project objects with lng/lat
 * @param {Object} buildingsGeoJson - GeoJSON FeatureCollection of buildings
 * @returns {Array} Projects with matchedBuilding property
 */
export function matchProjectsToBuildings(projects, buildingsGeoJson) {
  const results = [];

  for (const project of projects) {
    if (!project.lng || !project.lat) {
      results.push({ ...project, matchedBuilding: null, matchMethod: null });
      continue;
    }

    // Try exact match first
    let matched = findBuildingForPoint(project.lng, project.lat, buildingsGeoJson);
    let matchMethod = 'exact';

    // Fallback to closest building within 100m
    if (!matched) {
      matched = findClosestBuilding(project.lng, project.lat, buildingsGeoJson, 100);
      matchMethod = 'proximity';
    }

    results.push({
      ...project,
      matchedBuilding: matched,
      matchMethod: matched ? matchMethod : null,
      buildingArea: matched?.properties?.area_m2 || null,
      buildingConfidence: matched?.properties?.confidence || null
    });
  }

  return results;
}

/**
 * Create a GeoJSON with both projects and matched building footprints
 * For visualization on the map
 *
 * @param {Array} matchedProjects - Projects with matched buildings
 * @returns {Object} GeoJSON FeatureCollection
 */
export function createProjectsWithBuildingsGeoJSON(matchedProjects) {
  const features = [];

  for (const project of matchedProjects) {
    if (!project.lng || !project.lat) return;

    // Add project point
    features.push({
      type: 'Feature',
      properties: {
        id: project.id,
        name: project.name,
        type: 'project',
        hasBuilding: !!project.matchedBuilding
      },
      geometry: {
        type: 'Point',
        coordinates: [project.lng, project.lat]
      }
    });

    // Add matched building polygon
    if (project.matchedBuilding) {
      features.push({
        type: 'Feature',
        properties: {
          id: project.id,
          name: project.name,
          type: 'building_footprint',
          area_m2: project.matchedBuilding.properties?.area_m2,
          confidence: project.matchedBuilding.properties?.confidence,
          matchMethod: project.matchMethod
        },
        geometry: project.matchedBuilding.geometry
      });
    }
  }

  return {
    type: 'FeatureCollection',
    features
  };
}
