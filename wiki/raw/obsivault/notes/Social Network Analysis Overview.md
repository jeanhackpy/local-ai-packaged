## # Social Network Analysis

---

## created: 2024-06-24T19:20:59 (UTC +07:00)\
tags: [knowledge-management, social-network-analysis, graph-theory]\
source: <https://towardsdatascience.com/social-network-analysis-from-theory-to-applications-with-python-d12e9a34c2c7>\
author: Dima Goldenberg

# Social Network Analysis: From Graph Theory to Applications with Python | by Dima Goldenberg | Towards Data Science

> ## Excerpt
>
> Social network analysis is the process of investigating social structures through the use of networks and graph theory. This article introduces data scientists to the theory of social networks, with…

---

[

](<https://medium.com/@dimgold?source=post_page-----d12e9a34c2c7-------------------------------->)[

](<https://towardsdatascience.com/?source=post_page-----d12e9a34c2c7-------------------------------->)

Social network analysis is the process of investigating social structures through the use of networks and graph theory. This article introduces data scientists to the theory of social networks, with a short introduction to graph theory and information spread. It dives into Python code with NetworkX constructing and implying social networks from real datasets.

Article Outline

(This article is a written version of a talk from Pycon 2019. You can [watch the video](https://www.youtube.com/watch?v=px7ff2_Jeqw) below and [check the github code repository](https://github.com/dimgold/pycon_social_networkx))

[PyCon 2019 talk — Social Network Analysis](https://www.youtube.com/watch?v=px7ff2_Jeqw)

## Network Theory

We’ll start with a brief intro in network’s basic components: nodes and edges.

Example Network

**Nodes** (A,B,C,D,E in the example) are usually representing entities in the network, and can hold self-properties (such as weight, size, position and any other attribute) and network-based properties (such as *Degree*- number of neighbors or *Cluster*- a connected component the node belongs to etc.).

**Edges** represent the connections between the nodes, and might hold properties as well (such as weight representing the strength of the connection, direction in case of asymmetric relation or time if applicable).

These two basic elements can describe multiple phenomena, such as *social connections, virtual routing network, physical electricity networks, roads network, biology relations network* and many other relationships.

## Real-world networks

Real-world networks and in particular social networks have a unique structure which often differs them from random mathematical networks:

Source: [Huang, Chung-Yuan et al. “Influence of Local Information on Social Simulations in Small-World Network Models.” *J. Artif. Soc. Soc. Simul.* 8 (2005)](https://www.semanticscholar.org/paper/Influence-of-Local-Information-on-Social-in-Network-Huang-Sun/f3b6e274634bb6d1ed92ca3276e073244ad57dd1)

- [**Small World**](https://en.wikipedia.org/wiki/Small-world_network) phenomenon claims that real networks often have very short paths (in terms of number of hops) between any connected network members. This applies for real and virtual social networks (the six handshakes theory) and for physical networks such as airports or electricity of web-traffic routings.
- [**Scale Free networks**](https://en.wikipedia.org/wiki/Scale-free_network) with power-law degree distribution have a skewed population with a few highly-connected nodes (such as social-influences) and a lot of loosely-connected nodes.
- [**Homophily**](https://en.wikipedia.org/wiki/Homophily) is the tendency of individuals to associate and bond with similar others, which results in similar properties among neighbors.

## Centrality Measures

Highly central nodes play a key role of a network, serving as hubs for different network dynamics. However the definition and importance of [centrality](https://en.wikipedia.org/wiki/Centrality) might differ from case to case, and may refer to different centrality measures:

- **Degree** — the amount of neighbors of the node
- **EigenVector / PageRank** — iterative circles of neighbors
- **Closeness** — the level of closeness to all of the nodes
- **Betweenness** — the amount of short path going through the node

Illustration of various centrality measures. Source — [Arroyo, D.. “Discovering Sets of Key Players in Social Networks.” *Computational Social Network Analysis* (2010](https://www.semanticscholar.org/paper/Discovering-Sets-of-Key-Players-in-Social-Networks-Arroyo/a95793d5ce8e5370f1ef1c1b3d4c66cb02cfea39))

Different measures can be useful in different scenarios such web-ranking (page-rank), critical points detection (betweenness), transportation hubs (closeness) and other applications.

## Building a Network

Networks can be constructed from various datasets, as long as we’re able to describe the relations between nodes. In the following example we’ll build and visualize the [Eurovision 2018 votes network (based on official data)](https://eurovision.tv/story/the-results-eurovision-2018-dive-into-numbers) with [**Python *networkx***](https://networkx.org/) package.

We’ll **read the data** from excel file to a ***pandas*** dataframe to get a tabular representation of the votes. Since each row represents all of the votes of each country, we’ll **melt** the dataset to make sure that each row represents a single vote (*edge*) between two countries (*nodes*).

Then, we will **build a directed graph** using *networkx* from the edgelist we have as a pandas dataframe. Finally, we’ll try the generic method to **visualize**, as shown in the code below:

Eurovision network loading from excel file

nx.draw_networkx(G) outcome on Eurovision 2018 votes network

## Visualization

Unfortunately the built-in ***draw*** method results in a very incomprehensible figure. The method tries to plot a highly connected graph, but with no useful “hints” it’s unable to make a lot of sense from the data. We will enhance the figure by **dividing and conquering** different visual aspects of the plot with a prior knowledge that we have about the entities:

- **Position —** each country is assigned according to its geo-position
- **Style** — each country is recognized by its flag and flag colors
- **Size** — the size of nodes and edges represents the amount of points

Finally, we’ll **plot the network components in parts**:

The new figure is a bit more readable, and giving us a brief overview of the votes. As a general side-note, plotting networks is often hard and requires to perform thoughtful tradeoffs between the amount of data presented and the communicated message. (You can try to explore other network visualization tools such as [Gephi](http://gephi.github.io/) , [Pyvis](https://towardsdatascience.com/making-network-graphs-interactive-with-python-and-pyvis-b754c22c270) or [GraphChi](https://github.com/GraphChi/graphchi-cpp)).

## Information Flow

Information diffusion process may resemble a viral spread of a disease, following contagious dynamics of hopping from one individual to his social neighbors. Two popular basic models are often used to describe the process:

**Linear Threshold** defines a threshold-based behavior, where the influence accumulates from multiple neighbors of the node, which becomes activated only if the cumulative influence passed a certain threshold. Such behavior is typical to movie recommendations, where a tip from of one of your friends might eventually convince you to see a movie, after hearing a lot about it.

Linear Threshold activation function. Source: [The Independent Cascade and Linear Threshold Models.](https://link.springer.com/chapter/10.1007/978-3-319-23105-1_4) P. Shakarian, A Bhatnagar, A Aleali, E Shaabani, R Guo — Diffusion in Social Networks, 2015

In the **Independent Cascade model,** each of the node’s active neighbors has a probabilistic and independent chance to activate the node. This resembles a viral virus spread, such as in Covid-19, where each of the social interactions might trigger the infection.

## Information Flow Example

To illustrate an information diffusion process we’ll use the [Storm of Swords network](https://networkofthrones.wordpress.com/), based on Game of Thrones show characters. The network was constructed based on co-appearance in the “Song of Ice and Fire books”.

Schematic process of Game of Thrones network creation.

Relying on the independent cascade model, we’ll try to track down rumor spreading dynamics, which are quite common in this show.

Source: <https://www.pinterest.com/pin/753508581387517221/>

**Spoiler Alert!** Suppose *Jon Snow* knows nothing at the beginning of the process, while his two loyal friends, *Bran Stark* and *Samwell Tarly*, know a very important secret about his life. Let’s watch how the rumor spreads under the *Independent Cascade* model:

Independent Cascade process simulation code

The rumor reaches Jon at *t=1*, spreads to his neighbors in the following time-steps and quickly spreads all around the network, resulting in being a public knowledge:

Independent Cascade diffusion on Game of Thrones network

Such dynamics are highly dependent on model parameters, which can drive the diffusion process to different patterns.

## Influence Maximization

Source: <https://quizlet.com/398701664/flashcards>

**The influence maximization problem** describes a marketing (but not only) setup, where the goal of the marketer is to select a limited set of nodes in the network (**seeding set**) such that will naturally spread the influence to as much nodes as possible. For example, consider inviting a limited amount of influencers to a prestigious product launch event, in order to spread the word to the rest of their network.

Such influencers can be identified with numerous techniques, such as using the centrality measures we’ve mentioned above. Here are the most central nodes in *Game of Thrones* network, according to different measures:

Centrality Measures in Game of Thrones network

As we can see, some of the characters re-occur at the top of different measures, and are also well known for their social influence in the show.

By simulating the selection of most central nodes we observe that picking a single node of the network can achieve about 50% of network coverage — That’s how important social influencers might be.

Network influence coverage by different methods and budgets

On the other hand **Influence Maximization is Hard**. In fact it’s considered as an **NP-Hard problem**. Many heuristics were developed to find the best seeding set in an efficient calculation. Trying a brute-force method to find the best seeding couple in our network resulted in spending 41 minutes and achieving 56% of coverage (by selecting *Robert Baratheon* and *Khal Drogo*)- a result that would be hard to achieve with centrality heuristics.

## Wrap-up

Network analysis is a complex and useful tool for various domains, in particular in the rapidly growing social networks. The applications of such analysis include *marketing* i_nfluence maximization, fraud detection\_ or *recommender systems*. There are multiple tools and techniques that can be applied on network datasets, but they need to be chosen wisely, taking into account the problem’s and the network’s unique properties.

If you wish to cite this resource in your academic research, please use the following format:

*Goldenberg, Dmitri. “Social network analysis: From graph theory to applications with python.” PyCon 2019 — 3rd Israeli National Python Conference, Israel, 2019. arXiv preprint arXiv:2102.10014 (2021).*

## Useful Resources

## **Code and Data:**

- [Game of thrones dataset](https://github.com/jeffreylancaster/game-of-thrones) @jeffreylancaster
- [Networks tutorial](https://github.com/MridulS/pydata-networkx) @MridulS
- [Flags images](https://github.com/linssen/country-flag-icons) @linssen
- [Eurovision Data](https://eurovision.tv/story/the-results-eurovision-2018-dive-into-numbers)

## **Papers:**

- [Timing matters: Influence Maximization in Social Networks Through Scheduled Seeding — D. Goldenberg et al.](http://bigdatalab.tau.ac.il/wp-content/uploads/2018/07/timing-matters.pdf)
- [Active viral marketing: Incorporating continuous active seeding efforts into the diffusion model — A. Sela et al.](https://www.sciencedirect.com/science/article/abs/pii/S095741741830246X)
- [Maximizing the spread of influence through a social network — E. Tardos et al.](https://www.cs.cornell.edu/home/kleinber/kdd03-inf.pdf)
- [Efficient influence maximization in social networks — W. Chen et al.](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/weic-kdd09_influence.pdf)
- [Independent Cascade and Linear Threshold Models - P. Shakarian et al.](https://link.springer.com/chapter/10.1007/978-3-319-23105-1_4)

## Let’s stay connected!

Reach out to me with questions and ideas by [mail](mailto:dima.goldenberg@booking.com) or [Linkedin](https://www.linkedin.com/in/dimgold/).

Interested about my work at [Booking.com](http://Booking.com)? [Check out](https://booking.ai/) our

blog.