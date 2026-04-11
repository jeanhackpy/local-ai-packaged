---
title: ChatGPT
source: https://chatgpt.com/g/g-p-69731c5418fc8191bb3b0113b6e766e5/c/69106a60-65c0-8322-8a76-f206045c7c86
author:
  - "[[système **ontologique]]"
published:
created: 2026-03-29
description: ChatGPT is your AI chatbot for everyday use. Chat with the most advanced AI to explore ideas, solve problems, and learn faster.
tags:
  - clippings
---
Reflexion· typescript

import React from "react";

import { motion } from "framer-motion";

  

// Default export: single-file React component suitable for Vercel + Tailwind

// Usage: place this file in a Next.js page or a React app. Ensure Tailwind + Framer Motion are installed.

  

export default function ReflexionHome() {

return (

<div className="min-h-screen bg-white text-gray-800 antialiased leading-relaxed">

<div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">

<div className="flex items-center justify-between h-20">

<div className="flex items-center gap-4">

<div className="w-10 h-10 bg-gradient-to-br from-sky-600 to-indigo-600 rounded-lg flex items-center justify-center text-white font-bold">R</div>

<div className="hidden sm:block">

<span className="font-semibold">REflexion.asia</span>

<div className="text-xs text-gray-500">PropTech & Patrimoine — 🇹🇭 🇫🇷</div>

</div>

</div>

  

<a href="#investir" className="hover:text-sky-600">Investir</a>

<a href="#services" className="hover:text-sky-600">Services</a>

<a href="#destinations" className="hover:text-sky-600">Destinations</a>

<a href="#contact" className="hover:text-sky-600">Contact</a>

</nav>

  

<div className="flex items-center gap-3">

</div>

</div>

</div>

</header>

  

{/\* HERO \*/}

<main className="pt-24">

<section className="relative">

<div className="absolute inset-0 overflow-hidden">

{/\* background video / image placeholder \*/}

<div className="w-full h-full bg-\[url('/images/hero-drone.jpg')\] bg-cover bg-center opacity-80"></div>

<div className="absolute inset-0 bg-gradient-to-b from-transparent to-white/80"></div>

</div>

  

<div className="relative max-w-6xl mx-auto px-6 py-28">

<motion.div

initial={{ opacity: 0, y: 18 }}

animate={{ opacity: 1, y: 0 }}

transition={{ duration: 0.6 }}

className="grid grid-cols-1 lg:grid-cols-2 gap-10 items-center"

\>

<div>

<div className="inline-flex items-center gap-3 mb-4">

<span className="px-3 py-1 rounded-full bg-sky-100 text-sky-700 text-xs font-semibold">Investir en Thaïlande</span>

<span className="text-xs text-gray-500">Premium · Bilingue FR / EN</span>

</div>

  

<h1 className="text-4xl sm:text-5xl font-extrabold tracking-tight mb-4">

Investissement immobilier en Thaïlande —

<span className="text-sky-600"> performance & sérénité</span>

</h1>

  

<p className="text-lg text-gray-700 mb-6">

Optimisez votre retraite, développez votre patrimoine et générez des revenus passifs grâce à une sélection exclusive de projets et à des services tech‑driven pour professionnels.

</p>

  

<div className="flex flex-wrap gap-3">

<a href="#contact" className="inline-flex items-center gap-2 px-5 py-3 rounded-md bg-sky-600 text-white font-medium shadow hover:shadow-lg">

Commencer mon projet

<svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor"><path fillRule="evenodd" d="M10.293 15.707a1 1 0 010-1.414L13.586 11H4a1 1 0 110-2h9.586l-3.293-3.293a1 1 0 111.414-1.414l5 5a1 1 0 010 1.414l-5 5a1 1 0 01-1.414 0z" clipRule="evenodd"/></svg>

</a>

  

<a href="#destinations" className="inline-flex items-center gap-2 px-5 py-3 rounded-md border border-gray-200 text-gray-700 bg-white">Voir les biens</a>

</div>

  

<div className="mt-6 text-sm text-gray-600">

<strong>Offre B2B rapide:</strong> Pack marketing & IA pour conciergeries — lancement en 48h.

</div>

</div>

  

<div className="rounded-xl overflow-hidden bg-white/60 p-6 shadow-lg">

<div className="text-sm text-gray-500 mb-3">Diagnostic gratuit</div>

<h3 className="font-semibold text-lg mb-4">Quel est votre projet immobilier?</h3>

  

<form className="space-y-3">

<div className="grid grid-cols-1 sm:grid-cols-2 gap-3">

<select className="p-3 border rounded-md">