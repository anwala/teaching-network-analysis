# Homework 3 - Node centrality & Link analysis
**Due:** March 6, 2024 by 11:59pm
 *Read the entire assignment before starting.*

## Assignment

Write a report that contains the answers and *explains how you arrived at the answers* to the following questions. Before starting, you are encouraged to review the [Hubs Python Google Colab notebook](https://github.com/anwala/teaching-network-science/blob/main/spring-2023/week-4/data_340_02_s23_chp_03_hubs.ipynb). Name your report for this assignment `hw3_report` with the proper file extension.

A common use of the word "hub" in everyday speech is to describe airports that serve many routes (direct flights). Load the [OpenFlights US flight network](https://github.com/CambridgeUniversityPress/FirstCourseNetworkScience/raw/master/datasets/openflights/openflights_usa.graphml.gz) into a NetworkX graph to answer the following questions

(**Google Colab Report (1 point**)

### Q1 (1 point)

Draw the OpenFlighs US flight network graph. Ensure the graph is legible and pretty:
* Node labels are visible
* Edge crossings are minimized

### Q2 (1 point x 6)

* What is the average number of routes served by each airport in this network?
* What are the top five airports in terms of number of routes?
* How many airports in this network serve only a single route?
* Which airport has the highest closeness centrality?
* Which airport has the highest betweenness centrality?
* Compute the heterogeneity parameter of this network.

### Q3 (1 point)

Draw a network in which one node has a very high value of PageRank, although the same node has low closeness and betweenness centrality (don't forget to point out the node). Use a program to validate your results.

### Q4 (1 point)

The damping factor (*d*) in PageRank controls how of often (probability) that the random surfer follows one of the outlinks of the current page (node) vs. going to an arbitrary page (node) on the network.
(a) What does *d* = 0 mean? What would happen to the PageRank values in that case? Why?
(b) What does *d* = 1 mean? Can you explain a possible problem with using that value?

## Submission

Make sure that you have committed and pushed your local repo to your private GitHub repo (inside the `hw3` folder).  Your repo should include your report, images, and any code you developed to answer the questions.  Include "Ready to grade @anwala" in your final commit message. 
