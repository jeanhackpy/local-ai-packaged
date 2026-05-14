---
created: 2024-06-29T16:40:23 (UTC +07:00)
tags: [OSINT, obsidian, NLP, semantic-understanding]
source: https://medium.com/@farallon/uncommon-osint-obsidian-semantic-meaning-and-nlp-3339e1e51d70
author: Claudia Tietze
---

# Uncommon OSINT: Obsidian, Semantic Understanding and NLP | Medium

> ## Excerpt
> Learn how to turn Obsidian into an Open Source Intelligence (OSINT) investigation and analysis powerhouse using semantic understanding.

---
[

![Claudia Tietze](https://miro.medium.com/v2/resize:fill:88:88/1*A9GInIlndYMeMmYENX0a9w.png)



](https://medium.com/@farallon?source=post_page-----3339e1e51d70--------------------------------)

_At its heart, Obsidian is a note taking app, but in its soul, it is a chimera._

by Claudia Tietze: founder & managing director of Farallon, LLC

**Introduction**

Open Source Intelligence (OSINT) is defined by its sources — legal, open, public and commercial. It is vibrant, adaptable and has no set rules as to what tools a practitioner “should use” to uncover intelligence, organize it and make sense of it. We have a wide variety of choices for built-for-purpose tools with a heavy focus on collection. Yet there are many overlooked tools designed for completely different purposes that can be insanely useful for OSINT investigations, organization and analysis.

OSINT practitioners can be seen as a type of knowledge worker — melding logic, analytics and art. We answer questions and solve puzzles, then communicate in a way people can understand so they can make more informed decisions or integrate our findings with other knowledge.

I’m a multi-disciplinarian, cross-matching knowledge from one field and applying it to another. I believe that the tools we use are an extension of how we think, augment our minds and influence our thinking processes.

Knowledge is power. Data is currency. How we leverage the two is changing. Those are the shifts I explore by challenging others to think differently about the ways in which our technology can help us be better intelligence analysts and communicators.

This is the first article in the Uncommon OSINT series that highlight this multi-disciplinary approach with technology in a way that anyone can understand and use. Focusing on free or low cost tools, each article will demonstrate a use case, using specific examples and highlighting how the tool can be used for OSINT investigations and analysis. At the end of each article, I’ll give you all the information you need to get started with your own use case.

**_The Uncommon OSINT series of articles was inspired by a conversation with Amber at Tactical Tech’s Influence Industry Project. You can find the project here:_** [_https://influenceindustry.org_](https://influenceindustry.org/)

**_Focus:_** _Using Obsidian to draw out semantic meaning from data by adding context with inferred relationships to create new capabilities with Obsidian’s native features for use in Intelligence Analysis._

**Why Obsidian?**

We are on the [cusp of changes](https://www.youtube.com/watch?v=oE2YulyFRxE) in [how we interact with data and technology](https://forum.obsidian.md/t/personal-knowledge-graphs/69264) — how we think, make connections and learn. These changes orient our technical solutions more naturally toward how our brains work. We are used to — and comfortable with — the tools we’ve grown accustomed to over decades. It takes a little while to explore new ways of doing things to fully uncover their capabilities. In performing arts there is a saying: _It takes ten years to become an overnight success._ The same is true for the evolution and adoption of technology. When our tools are ‘good enough’, we use them habitually instead of looking for innovative approaches that can surface fresh ways of uncovering insight.

This shift led me to explore Obsidian — a free-flowing note taking app structured toward ideas and concepts instead of chronology and folders. Last year I challenged myself to turn Obsidian into an OSINT tool that allows me to discover contextual connections that are hard to uncover without expensive sophisticated technological assistance.

I took a perfectly beautiful note taking tool, and then I broke it… and I couldn’t be happier with the results!

Since then, I have used Obsidian to anticipate unknown locations of Ukrainian children transported to Russia, map out corporate structures, track espionage, identify money laundering, analyze theoretical intelligence, and explore the mystery of the Baltic jammer. Obsidian is an OSINT multiplier.

![The Obsidian app offers links, graphs, canvas and plugins](https://miro.medium.com/v2/resize:fit:700/1*4og5-UXkzyTv5EaOLjrPJA.png)

Obsidian offers bi-directional notes, graphs, infinite canvas and community plugins. It a flexible and scalable note taking app that focuses on relationships between your notes over time to draw out points of meaning. \[image source: [Obsidian website](http://obsidian.md/)\]

**USE CASE TOOLS**

**Obsidian:** Open source, platform agnostic, and free for individual use with optional paid services that add convenience to some actions like sync or publishing. Low cost commercial use. Uses Markdown. Adaptable and scalable with an enthusiastic community and community plugins. There is excellent [documentation](https://publish.obsidian.md/hub/00+-+Start+here) and [community support](https://obsidian.md/community) for Obsidian to help you learn. If you get stuck or want to bounce an idea off someone — feel free to reach out.

**What makes Obsidian special?** At its heart, Obsidian is a note taking app, but in its soul, it is a chimera. What you can imagine, you can create. Unshackled by traditional hierarchy structures, Obsidian focuses more on the significance and nature of relationships between one or more notes throughout all the bits of knowledge you’ve collected. Obsidian lives in a constant state of controlled entropy.

**Why I chose it:** The scant few write ups that exist about using Obsidian for OSINT are too limited. They miss the bigger powerhouse features that can elevate investigation and analysis.

**Key Concepts and Definitions:** While you need little to no technical expertise to put this use case to work, I’m going to explain some definitions and concepts so we can speak a common language. If you aren’t interested, you can skip down to the _Onward!_ section.

-   **Digital Garden:** Obsidian was developed as a digital garden, using linked ideas to reveal connections by reducing the friction of networked thinking. It was developed to keep short notes over time that evolve with us — as we learn, grow and change. Digital gardeners are hands-on; tending our gardens over time. Just like a real garden, a digital garden is planted, cultivated, curated, nurtured and interacted with season after season. And just like gardening, it’s messy, full of surprise and wonderment; and no matter how much we plan, a garden thrives in its own beautiful chaos, even as we hope that our patience and diligent care will pay off.

![](https://miro.medium.com/v2/resize:fit:700/0*koOBapaVCBV6UMOF)

Photo by [Markus Spiske](https://unsplash.com/@markusspiske?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com/?utm_source=medium&utm_medium=referral)

-   **Knowledge graph:** The connections in Obsidian can be used to create a knowledge graph built on structured representations of information that capture relationships between entities with an emphasis on connected data and semantic meaning. This approach is shown to enhance decision-making and strategic planning by providing a [comprehensive view of information and relationships](https://www.ontotext.com/blog/the-importance-of-the-semantic-knowledge-graph/). And it’s the approach we’ll be taking in our use case.
-   **Semantics:** The study of the meaning of words and phrases in language. The primary goal of semantics is to give context to data. By doing so, data transforms into actionable knowledge. Semantic data empowers us to move beyond mere numbers and embrace the deeper context that drives informed decisions and innovation. We are going to add semantic data for our use case with [Wikidata](https://www.wikidata.org/wiki/Wikidata:Main_Page).
-   **Ontology:** Standard definition for knowledge; defining relationships between terms and concepts. They create a shared understanding of domain-specific knowledge. Semantics are a large part of ontologies by providing relationship information.
-   **Triples:** Structured statements about information which are used in semantics. Using subject-predicate-object construction, relationships between and among entities are explained and defined by the properties that describe them. Triples are fundamental to encoding information in a semantic-based knowledge graph.
-   **Semantically Inferred Relationships:** Using Transitive Reasoning semantics helps a machine make inferred connections using: If A is related to B and B is related to C, then A is indirectly related to C.
-   **Vault:** A vault in Obsidian is a collection of notes and data. You can have multiple vaults. In OSINT terms, you can create a vault for each case.
-   **Note:** Each entry in your vault is a note. A note is like a page in a notepad that may or may not embed other file types in it. Each note has a title and a body and can have front matter (YAML), which adds more information about that note’s contents and nature.
-   **YAML/front matter:** For our purposes, YAML, or front matter, serves as a way of describing our note. Think of it like a driver’s license. Very quickly we can relay who we are, that we are who we say we are, and certain biographical information about us. For our use case, YAML is where we will add information that explains our note’s place in the world by incorporating Wikidata. Our use case YAML could be considered metadata on steroids.
-   **Backlinks:** Incoming links from other notes.
-   **Outgoing links:** Links going to other notes.

**Skill level:** Medium.

If you are beginner, getting used to Markdown and YAML might take a little while. Once you get it, it will be a snap! Everyone’s preferred organizational and formatting style will be different.

**Security level:** Customizable from highly secure to loosey-goosey

-   Cloud or desktop
-   Encryption options available
-   Community plugins are open source with the code reviewable on GitHub for security concerns.
-   Some plugins call third-party services where your data may be exposed. In some cases, there are alternative options that live on your machine and don’t expose your data.
-   Restricted Mode turns on/off plugins for troubleshooting conflicts or keeping your vaults secure and sequestered. For our use case, once we import the semantic information, you can run some of the analysis in Restricted Mode using native Obsidian features. If you decided the plugins are too exposed for a secure case, you should consider populating the Wikidata terms first, locking down your vault and then adding case file data.

**USE CASE:** Intelligence Playground Vault

Applying semantics is a method I use to augment existing data. This use case solely focuses on how you can augment your data with semantic understanding and demonstrates a few enhancements and visualizations based solely on this enrichment.

Our vault is called Intelligence Playground because I began by using intelligence terms and enhanced them with connections made from Wikidata that Obsidian surfaced. The goal is to show you how maximizing the use of YAML front matter with Wikidata can help make connections and reveal inferred relationships.

![YAML for analytical technique on left. Network graph of note reveals inferred relationships that are not found in the YAML](https://miro.medium.com/v2/resize:fit:700/1*8R5lXmerBj5ZPNKsQXa7xA.png)

An example of how this combination of Obsidian and semantic data can reveal inferred relationships. On the left all the YAML for analytic technique is revealed. \[subclass: intelligence analysis, studied in: analysis, uses: geopolitics, intelligence and strategy\] Without direct mention, our Obsidian vault correctly inferred that analytic technique is an instance of PESTLE analysis.

**Onward!**

Now that we have a common language, let’s take a look at our use case and how to set up our vault.

**Laying the foundation — our data**

-   Add Wikidata entities to populate YAML
-   Add Wikpedia articles to the body of some notes for text examples
-   In cases where the Wikidata description was not specific to intelligence, add additional YAML by hand. (This is usually solved with topic-specific ontologies, and Wikidata is a generalist.)

**Add Wikidata**

Wikidata includes over [100 million data items](https://www.wikidata.org/wiki/Wikidata:Main_Page) in semantic web structured format, so it’s a great starting place. On the website, Wikidata breaks down information into various categories in multiple languages. This is what an entry in Wikidata looks like on the webpage:

![Wikidata entry page](https://miro.medium.com/v2/resize:fit:700/1*d29b-0yogRJ-JuKJ_NoQHg.png)

WIkidata entry page. The Wikidata Importer plugin allows you to select whether you want all the identifiers to be imported (this can get very long and sometimes causes delays) or select other options for your needs.

To add Wikidata to the Intelligence Playground vault, we’ll use the Wikidata Importer plugin by Sam Rose.

We start by entering the term we want to import into the interface for the plugin. I chose “spy”. Then select the result that most fits what you want to include in your vault.

![Intelligence Playground Vault Wikidata Importer plugin interface selecting “spy”](https://miro.medium.com/v2/resize:fit:700/1*2HVBv2e9foBJ0DBl6l5ZNg.png)

_Intelligence Playground Vault Wikidata Importer plugin interface. This allows you to see and select the concept that you want to import. If you don’t see a good option, you can alter your search term or import the definition closest to your subject matter and fine-tune it with your own YAML pruning and cultivation._

In the screenshot above you can see that “spy” has several options, including specific events, locations and pop culture references. It will sometimes include papers or news articles. One thing to keep in mind: _Obsidian does not allow certain characters in titles, so data with a colon will fail to import. If you feel you need a particular source, you’ll need to find another method of importing it._

Once you have imported your term, it will populate entries into the YAML — adding layers of intelligence.

![Wikidata import to YAML for term “spy”](https://miro.medium.com/v2/resize:fit:700/1*7Gy6E0CrYsw-KF7rHOJAyA.png)

_Part of the indicators imported as YAML from Wikidata for the term spy. Once imported, this populates the YAML of a note. You can see that it designates a spy as a subclass of an intelligence agent and that the field of the occupation of a spy is espionage._

In the above screenshot you can see some indicators, but also international translations and even the spy emoji 🕵.

**Adding Wikipedia articles**

To add Wikipedia articles, we will use the Wikipedia plugin by Jonathan Miller. This will import the first section of a Wikipedia article into your note.

![Wikipedia text for “spy” added to the body of a note](https://miro.medium.com/v2/resize:fit:700/1*O_rVMO17HkyO6wne-t-hCA.png)

_Adding Wikipedia text to the body of a note lets us make bi-directional connections between notes through the text. It also gives us more context about topics, ideas and concepts. The text in the body of notes can be anything and is not limited to things like Wikipedia._

If this were not a limited use case, we might have other information in the note, such as statistics, records, filings, articles, highlights from reports or whatever you collected that you want to connect in your vault. We make those connections with bi-directional links — both incoming and outgoing.

These links let us see how our notes are connected to each other and reveal the information the other notes have about our topic. You’ll notice two sections — Linked mentions and Unlinked mentions. Unlinked mentions are just things we have not “officially” linked yet but exist in our vault. These require hand-review and approval. They will show the term in headings and URLs. You don’t want to link to a concept in a URL as it will break the link by adding Markdown \[\[double brackets\]\] around the term. Whether you link to headings is a matter of preference.

![Linked mentions for “spy”. This shows lines with title and instances of spy in other notes YAML (specific to this use case)](https://miro.medium.com/v2/resize:fit:700/1*w76L5R-JiyPebauKEK4jGA.png)

In Obsidian, linked mentions are those made between a concept in a note and either text in the body of another note or found in the YAML of other notes.

In this case, all the linked mentions are very short with no descriptive text. This is unusual and is only happening due to our limited scope. The linked mentions are connected to the YAML we imported from Wikidata. In other words, these links already exist in our vault and have been confirmed.

Usually your mentions — linked or unlinked — will contain text from the body of a note.

![Unlinked mentions also showing text and the word “spy” highlighted in the body of another note.](https://miro.medium.com/v2/resize:fit:700/1*alYj7VEa8TL5xCUMdrLhnw.png)

In Obsidian, unlinked mentions are other notes and YAML that exist in the vault, but the link between them has not yet been created. Once they are “officially” linked, two notes will be connected bi-directionally, and they will move up to the linked mentions section.

If you look at the unlinked mentions, you’ll notice a text passage, and the word “spy” highlighted. This gives us more context when we link the two notes using \[\[double brackets\]\] by hand, or selecting the “link” button available in the unlinked mentions pane. Once the body text is linked, it will show up in our note and also as a connection with text context in the other note. The links and context flows both ways between notes.

**The Fun Stuff**

Now that we have our vault set up and populated with terms about intelligence from Wikidata and a little bit of Wikipedia, what can we do with this stuff?

**Analysis — Explore and communicate our data**

-   [Network graphs](https://osintdrip.substack.com/cp/143786715)
-   Natural Language Processing
-   Clustering and topic modeling alogrithms
-   Charts and graphs

Since Obsidian is all about making connections, network graph capability is native to the platform. We’ve enhanced this with a few extra plugins.

Graph Link Types by natefrisch01 adds link type information between two nodes on your graph such as “related to” “product of”, etc. This plugin also adds color coded relationship lines and a legend.

Juggl by Emile van Krieken grew from the same backbone ICIJ uses to visualize their [Off Shore Leaks](https://www.icij.org/investigations/paradise-papers/) project — [Neo4j](https://neo4j.com/product/neo4j-graph-database/). This adds interactive stylability to your network graph.

Now let’s explore!

You can explore the graph of a single note one level deep. You can keep your note on one side or top/bottom orientation.

![One level with split pane note on left and one level deep graph on the right.](https://miro.medium.com/v2/resize:fit:700/1*FHhP6cjNDAKPhDe94gDIZQ.png)

_Obsidian works with panes — you can have multiple views combining files, notes, graphs, canvases and other workspaces. This shows the body of the spy note on the left, and the one level direct relationship graph of the same note on right._

Alternatively, you can close all other panes and only view the network graph. Here we’ve selected only the most direct incoming and outgoing links.

![Single note one level network graph with incoming and outgoing links. Also shows toggle bar on right for filters.](https://miro.medium.com/v2/resize:fit:700/1*kt7hVWZ6QY0lTwuJ9GnYkg.png)

_Single note showing one level network graph with only incoming and outgoing links. This only shows the direct relationships to our note. As a side note (if you are a geek like me and actually read captions give a shout out) you can color code your nodes, set how much resistance there is and how to display your graph._

We can include neighbor links as well. If you think of “spy” as you, and the direct connections as your closest inner circle of friends, neighbors are part of your friends’ close circle of people but only in a limited context (say, a party). They are connected to you through your besties whether you are close to them or not. However, you are aware of them and their relationship to your closest friends. In essence, neighbors expand your circle of connections but only within a limited context. They only interact with your besties in this specific setting.

![Single note one level network graph with incoming and outgoing links plus neighboring links. Shows toggles on right side for filters.](https://miro.medium.com/v2/resize:fit:700/1*A0nK1_5q97uCdSsrgBS6gw.png)

_Single note one level network graph with incoming and outgoing links plus neighboring links. This reveals direct neighbor connections to the immediate one-level graph of a note. This helps us see relationships in context that other notes have to the direct links of our note._

Notice some of these connections have a description of the relationship on the line between two nodes. This is what Nate’s Graph Link Types plugin does for us. It also gives us the color-coding of the relationships, and you can see the legend of the meaning on the upper left.

If we want to expand even deeper, we can change the depth from one level to two levels with or without neighbors. I chose without neighbors for more simplicity. This is removes the limited context above (a party). The way to think of this is your BFF giving you their address book. You aren’t going to call these people and don’t interact directly, but you have your BFF in common, and your network expands. If we had added neighbors, that would give us additonal context and proximity to you (the spy).

![Single note one level network graph with incoming and outgoing links two levels deep. There are many more connections. Filter toggle is on the right side.](https://miro.medium.com/v2/resize:fit:700/1*S-_ZHe6rA3DIoYPnXYMF6w.png)

_Single note one level network graph with incoming and outgoing links only, but expanded to two levels deep. Two levels deep lets you see more interconnectedness between multiple notes in your graph. The measure of depth is a slider. Default is one level deep._

The graph is interactive, so when we run our cursor over certain nodes, the connections light up for us. Here, we can see that a spy is connected to an intelligence agency, and through that connection, a spy is also connected to intelligence agent, covert operations and espionage.

![Interactive network graph highlighting a specific node and its relationship. This shows intelligence agency as a hub node that connects the node for spy to other nodes.](https://miro.medium.com/v2/resize:fit:700/1*cMSNd0FFgK_SrZiZgSX0jg.png)

_An Obsidian interactive network graph can reveal specific relationship pathways by highlighting a specific node to reveal its relationships. In this case, intelligence agency had several connections, so it was selected, revealing that a spy has other relationships through the intelligence agency commonality._

We can also see the direct connections from each of those nodes, expanding our understanding.

When we want more control over our graph, that’s where Emile’s Juggl plugin comes in.

![Network graph visualized with Juggl plugin. It shows a network graph with different colored nodes, some have larger triangles and some have icons.](https://miro.medium.com/v2/resize:fit:700/1*R0s83g8PDLbLM-POvOlMDA.png)

_Network graph visualized with Juggl plugin with custom assigned shapes. colors and icons. You can assign these representations by their property type found in YAML. For example, all countries can have their own schema (countries are circles and green or have an assigned icon) for easier visual identification._

Within Juggl, you can assign icons, shapes and colors, assorted views and other customizations. Juggl enchances the capabilities of your graph view. When you select a node, the note in focus will change to the corresponding note, and the graph re-orients itself to that note.

![Interaction with network graph visualized with Juggl plugin. This graph focuses on espionage as the graph re-orientated itself based on the node I selected.](https://miro.medium.com/v2/resize:fit:700/1*UV6us-MiiFNYmRaOgTwqPg.png)

_Interaction with network graph visualized with Juggl plugin. By selecting a node — espionage — we see a reorientation of the graph focusing on the espionage note and graph._

If I want to explore espionage more fully, I can do this in several ways, including breaking away just a single connection.

![Breaking out a specific node in network graph with Juggl plugin. Shows focus on operational cover with only the first level connections to it.](https://miro.medium.com/v2/resize:fit:700/1*eZnlS1qDsK_6-C0fzU40rw.png)

_You can break out a specific note in the Juggl network graph by hovering over the note and right-clicking for menu options. This lets you explore the graph on a more granular level._

What if I don’t want to go back to my note or keep it open to learn more about a node? Then I can call up any text that exists in a note by putting my cursor over those that indicate there is more information.

![Network graph with info box. Cursor over the node “encryption” offers the popup of the contents from the encryption note.](https://miro.medium.com/v2/resize:fit:700/1*GvtEW7_r5Myakh5ISByZ6Q.png)

_By hovering over a note in the Juggl network graph, an info box pops up to reveal the text found within the body of the note._

**Drawing Meaning from Algorithms**

When you launch your vault, it is indexed and analyzed by SkepticMystic’s NLP plugin (NLP = Natural Language Processing). This extracts entities and parts of speech, and breaks down the text in your vault into bite sized pieces using tokenization to help the machine understand it better.

After the NLP plugin does its thing, the Graph Analysis plugin by SkepticMystic and Emile allows us to explore a note with multiple different topic modeling and clustering algorithms. This helps us see different ways the topic of our note is connected to other concepts within our vault, or the intelligence in our whole vault, using a variety of algorithmic techniques.

In this example, we are viewing the results of the HITS algorithm. HITS stands for Hyperlink-Induced Topic Search. It was developed for ranking webpages based on whether a page is a hub for other information and how authoritative it is.

![HITS algorithm results with Graph Analysis plugin — shows note text for spy on left and a list of HITS on the right with weights. The top five read: espionage, intelligence agency, counterintelligence, secrecy and counter-terrorism.](https://miro.medium.com/v2/resize:fit:700/1*Ms3GheplBTNAKY7OYkP1gw.png)

_HITS algorithm results with Graph Analysis plugin showing weights for both authority and hub. The higher both scores are, the more significance is given to that result. Above, the score for espionage is the highest._

In this case, it’s showing us links in our vault to notes that serve the largest number of connections and have high-quality content. You can see the authority and hub scores on the far right after the terms. _These results might be skewed in our use case because we did not add Wikipedia to every note available. It’s possible additional text in the body of a note affects the results._

The Jaccard algorithm shows us how much two notes have in common. You can see the quality score on the far right column after the terms.

![Jaccard algorithm results with Graph Analysis plugin. Body of the note for spy is on left and on the right is a list of Jaccard results with weights. The top five are: double agent, official cover, espionage, entryism and intelligence agency.](https://miro.medium.com/v2/resize:fit:700/1*J93t4DyxiY-KiKCKBFs7aQ.png)

_Jaccard algorithm results with Graph Analysis plugin shows us commonality between two notes. The score on the right shows how much two notes have in common._

In a real case, the Jaccard algorithm can be used to find companies in corporate structures that have not yet been identified as significant but have a high degree of similarity. Depending on the contents of your vault, it can be used as a clue to look deeper at those two corporations for common ownership or shared activities.

**The Magic of the Canvas**

[Canvases in Obsidian](https://obsidian.md/canvas) are a workplace where you can create your own material like diagrams, cards or charts and graphs on an infinite canvas. You can brainstorm, make your own connections by hand, group cards, add color or images, create visuals for communicating ideas, and move things around in a free-flowing manner.

For our use case two plugins will create our starter canvas — Link Exploder by Ben Hughes and Semantic Canvas from Aaron Gillespie. Once we have the start from the plugins, we can add all sorts of information from our vault that we want to visually link.

**_OSINT TIP:_** _This is great for generating part of a report in an actual case, gaining clarity or gaming out hypotheses._

Ben’s Link Exploder plugin shows the incoming and outgoing links to/from a note and the corresponding notes on a canvas with cards. From our spy note, we’ll select the command center and choose Link Exploder.

![Link Exploder plugin in command center. This shows a list of options, one of which says LINK EXPLODER Create Canvas from File Links.](https://miro.medium.com/v2/resize:fit:700/1*S40s6Xp9bXEeAzhztiMXkA.png)

_Link Exploder plugin in command center. By selecting Create Canvas From File Links, we create a canvas with cards and connections showing incoming and outgoing links._

**_OSINT TIP:_** _If you create a note called IP Addresses and other notes containing all IP addresses found in your case, linking those together using YAML or the body of the notes, you could create an instant canvas showing all IP addresses and their connections to each other. You could also do this with YAML by assigning “kind” or “type” or “IP Address” to notes._

Our starter canvas is automatically populated. Since it’s the index of our vault, our starter canvas included the file \_Index\_of\_Intelligence\_Playground. It isn’t significant, so we’ll remove it from the canvas by selecting the trashcan in the menu that pops up when we interact with the card.

![A canvas with several cards organized with lines as links to spy or other cards. On the _Index_of_Intelligence_Playground card, a menu pops up showing different options, including delete.](https://miro.medium.com/v2/resize:fit:700/1*6XiDleSEqUBLcu5Ik8Wy3g.png)

_Removing cards in a canvas is easy. Hover over the card and hit the trash can icon. You can also add color to external frames or internal ones in a group, search and add a note from the same menu._

Now we’ll select some colors to make our canvas stand out and help us visually organize it. I assigned yellow for hubs, blue/green for descriptors and purple for things that potentially have action or risk associated with them. I moved things around so I could get a better picture.

![The same canvas with right hand side card group moved around and the cards color coded.](https://miro.medium.com/v2/resize:fit:700/1*zPsz6HjVovheFUD2I7NptA.png)

_Color coding and moving cards in canvas is easy. Colors are selected from the icon menu when you click on the boundary of a card. Moving cards, or groups of cards, is as easy and dragging them into their new position._

From the menu, either bottom center or right click from a specific card, we can add a card, a note from the vault, media from the vault, a website or create groups of cards. I added some pictures and a card with thoughts on it and dragged links to connect to other cards.

![Added 3 images and a card I wrote a note on to the canvas. Linked those with other cards easily by dragging the line from one to the other.](https://miro.medium.com/v2/resize:fit:700/1*d-M3sA4PMuxtKKKzs1eF3A.png)

_Adding pictures and cards in canvas is easy. There are two ways to access the menu — either a limited menu prominently bottom center, or from each card via a right click menu. Once you add your own cards or images, you can easily link them from any of the four sides to any other four sides of another asset on the canvas._

When we zoom in, we can see the information found in notes that have text in the body and examine the ideas in more detail with our Link Exploder spy canvas.

![Zoom in canvas reveals that cards belonging to notes that have text reveal that text and notes that do not have text remain blank with only the title visible.](https://miro.medium.com/v2/resize:fit:700/1*NY7K9MHm3JAsiyAy5t2lJg.png)

_Zoom in on canvas reveals more context. Notes that have text in the body show the text. Notes do not contain text show the title of the note. We can also more easily see the directional arrow of a relationship._

You’ll notice some of the cards are blank and don’t have a note description. That’s because there is no text in the body of those notes yet.

Aaron’s Semantic Canvas plugin isn’t interested in relational links in the same way. It focuses on the semantic structure of a concept.

![](https://miro.medium.com/v2/resize:fit:700/1*AAkMO9q5yM9uC8t3jSBypg.png)

_Semantic Canvas plugin reveals the semantic structure of language and triples are shown on the lines of the links between two cards to add context to relationships between two or more concepts (cards)._

And if you zoom in, you’ll notice some notes don’t have information. Those notes have a menu inside of them that we can interact with.

![Zooming into the Semantic Canvas reveals menu choices in the cards with no words. These are notes that have not been created yet. The choices are Create New Note, Swap and Delete.](https://miro.medium.com/v2/resize:fit:700/1*xzpq8ZYMwAgUSF2j3eQ-8A.png)

_Semantic meaning canvas — using card menus allows us to add more information on the fly specific to our interests in a more graphical way. We can access a menu on an empty card — these are notes that do not yet exist but where a semantic link has been identified. The menu lets us create a new card, swap this card for another from our vault, or remove it._

This shows us semantic connections from the YAML, whether or not the note has been created. If we want to create a note, we can choose create new note, swap the file or remove it. This can be a great way to build out concepts using the canvas. Aaron’s plugin also lets us append a note from our canvas, so any work we do here, we can add to the knowledge in the note itself.

If the Wikidata YAML has a link to an image, the Semantic Canvas plugin can add the image automatically. Below is an example. I did not add these images. They were pulled from the image hot links in the YAML provided by Wikidata.

![Semantic Canvas showing geopolitics linking to two notes with text — political geography and global politics — and two images of maps. The cards are colored with geopolitics in red, the two text cards in blue and maps surrounded in a group by purple.](https://miro.medium.com/v2/resize:fit:700/1*3raQ9ZUNFWcesRpx1sX02A.png)

_Including images from YAML in canvas is automatic if that option is selected in the plugin settings. These images are pulled from image URLs found in the YAML inserted by Wikidata._

**Charts and Graphs**

It’s often helpful to visualize a complex investigation in many different ways. I added another plugin to create some charts to help us do that. Charts View by Caronchen lets us play with plots and graphs either from our vault data or imported from a file. We can embed those charts into our notes.

![Shows chart menu options: bar, pie, word cloud, word count, treemap, dual axes, mix, organizational tree graph, radar, tiny line and scatter](https://miro.medium.com/v2/resize:fit:700/1*O5_MhmUNOU3j2scCk5k7tA.png)

Charts View plugin chart options that include pie, bar, word cloud, word count, treemap, dual axes, mix, organization tree graph, radar, tiny line, scatter plots and dataviewjs example columns.

**_OSINT TIP:_** _Charts and graphs are helpful for report writing._

I chose two chart options — word cloud and foam tree.

![Word cloud](https://miro.medium.com/v2/resize:fit:700/1*vWdd4it0W_RgZggQAN7_tw.png)

_Word cloud chart with Charts View plugin allows you to set relevance._

![Shows colored tree chart embedded under the Wikipedia text for spy.](https://miro.medium.com/v2/resize:fit:700/1*4fa7-GZIUraJZpdhdxhTgA.png)

_The Chart View plugin can embed cart within a note — in this case a foam tree chart._

**But How Can I Use This For Actual OSINT Stuff?**

Links between things can be anything. Technology is agnostic. Tech doesn’t care if you are exploring the Intelligence Playground, collecting recipes or looking at money laundering. It’s all about data points and connections between them, no matter what that data is.

The YAML categories from Wikidata include identifiers significant for an OSINT investigation. This covers everything from events and cyber to people and companies to countries and politics. These critical investigative identifiers are enhanced by any reports, documents, articles, text or images added to your case file for analysis.

![](https://miro.medium.com/v2/resize:fit:514/1*7VCZHPiN7frtTfUAO4oKuw.png)

Wikidata provided YAML includes identifiers specific for OSINT such as: images of logos or seals, headquarters locations, awards received, whether an organization has a subsidiary, if a person or organization is a member of something, where archives can be found, who a chairperson is and what parts something has. Other YAML includes social media profiles and follower count, significant events, more societal positions, etc..

**Other Things to Keep in Mind for OSINT**

-   You can create your own YAML to suit your use case and preferences.
-   Adding event dates and geodata can be used to create timelines (yes, Obsidian does this) and maps (yup, that too).

EXAMPLE: For a different use case tracking the recent slew of Russian espionage cases, I added my own YAML. I wanted to identify relationships outside of direct spy cells — such as a real life husband and wife Russian spy couple who work in different countries apart from one another and are not connected through their cover identities.

![Three panes — the far left shows YAML options, middle shows the custom YAML in a note on spy Roussev and on the right pane, unlinked mentions.](https://miro.medium.com/v2/resize:fit:700/0*KmjWtLp8IwXLD29V)

Espionage vault example of how to add custom YAML that fits your use case and helps you answer the questions you want answers to. In this case, to identify commonality between spies and cells, I added the location the spy was in when caught, biographical data, affiliates, co-conspirators, whether it was an individual or a spy cell, handler, which intelligence agency they worked for, their cover legend (if any), citizenship, any countries they were active, businesses and what sort of spy activity they engaged in.

-   Aliases are important. They help link all representations of an idea literally or subjectively, to other notes found in your vault. An alias that includes alternate spellings and acronyms helps us identify all variations we come across.
-   Subjectively linking concepts using aliases can be helpful in some cases for simplifying many moving parts. For example, railway can have all terms associated with railways, trains, etc. Or all types of transportation can be aliased under one note.
-   Foreign language cases also benefit from Wikidata since it is available in over 300 languages. Using your aliases for other language variations of names is powerful. Using this methodology, it is effective to run multi-lingual cases.
-   Canvases can be a fast way to do a flow chart for corporate structure, brainstorming or to map out a ring of people. You can append those and embed them into notes or use images of them in reports.

**Conclusion**

As OSINT practitioners, we have a wide variety of tools at our disposal — so many that sometimes we forget to look around us and explore other tools built for other purposes.

The capabilities I showed you — the ones you can draw out of Obsidian — I’ve encountered in expensive custom big data builds and commercial products. Your cost for these added capabilities as an individual is your time, curiosity and creativity. If you are an enterprise, please make sure to buy a [commercial license](https://obsidian.md/pricing) from Obsidian. These cost $50 per user per year. No fuss, no muss licensing. It helps support the continued creation of this amazing tool.

**What You Need To Get Started**

-   **Platform: _Obsidian_** downloadable from [Obsidian](https://obsidian.md/) or [GitHub](https://github.com/obsidianmd)
-   **THEME:** The theme tested with this plugin combination is the LYT theme by Nick Milo. I can’t guarantee other templates will behave the same way. Themes can interfere with how your vault is displayed and cause conflicts with plugins. If you run into issues, revert to default.

**_Be sure to back up your vault. When a conflict arises, it’s possible to lose data._**

**Plugins:** _Some plugins are dependencies to make others work, and some are to keep your vault organized and neat._

**Administrative Plugins**

-   **_Zoottelkeeper_** _by Ankos Balasko:_ It maintains index files in all of your folders in your vault; if you create/delete/move a note, the index files will be updated automatically. It can be used to show folder in Graph View.
-   **_Linter_** _by Victor Tao:_ Format and style your notes. Linter can be used to format YAML tags, aliases, arrays and metadata; footnotes; headings; spacing; mathblocks; regular Markdown contents like lists, italics and bold…

**Dependencies**

-   **_Dataview_** _by Michael Brennan:_ Advanced queries over your vault for the data-obsessed.
-   **_BRAT_** _by TfTHacker:_ Easily install beta versions of a plugin for testing.
-   **_NLP_** _by SkepticMystic_: In **BRAT** you will import _SkepticMystic’s_ **_NLP_** plugin.

**Enrichment**

-   **_Wikidata Importer_** _by Sam Rose:_ Import data from Wikidata into your vault.
-   **_Wikipedia_** _by Jonathan Miller:_ Get the first section of Wikipedia for a note title or search term.

**Analysis**

-   **_Charts View_** _by Caronchen:_ Visualize data from your notes with plots and graphs. (You can import files as well.)
-   **_Juggl_** _by Emile van Krieken:_ Add a completely interactive, stylable and expandable graphview.
-   **_Graph Analysis_** _by SkepticMystic and Emile:_ Find hidden connections in your vault using cool graph algorithms.
-   **_Link Exploder_** _by Ben Hughes:_ Link Exploder creates a canvas from a note, embedding its incoming (i.e., backlinks) and outgoing links onto the canvas (as well as their linked notes).
-   **_Graph Link Types_** _by natefrisch01:_ Link types for graph view.
-   **_Semantic Canvas_** _by Aaron Gillespie:_ Create semantic knowledge graphs using canvases to modify note properties graphically.