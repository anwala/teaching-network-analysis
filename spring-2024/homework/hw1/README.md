# Homework 1 - Network Elements/Analysis Toolkit
**Due:** Tuesday, February 15, 2024 by 11:59pm
 *Read the entire assignment before starting.*

## Assignment

Write a report that contains the answers and *explains how you arrived at the answers* to the following questions. Ensure to show any intermediate calculations. Before starting, review the [HW report guidelines](https://github.com/anwala/teaching-network-science/blob/main/spring-2023/homework/hw0/README.md).  Name your report for this assignment `hw1_report` with the proper file extension.

(**Google Colab Report (1 points**)

### Q1 (3 points)

Go through the [tutorial on Network elements](https://github.com/anwala/teaching-network-science/blob/main/spring-2023/week-2/data_340_02_s23_chp_01_network_elements.ipynb).

Implement functions for Exercises 1 -- 3    
    
### Q2 (1 points)

Consider this adjacency matrix.

<img src="adj_mat.png" alt="Ajacency matrix for hw1 Q2" height="200"><br/>

An entry in the *i*th row and *j*th column indicates the weight of the link from node i to node j. For instance, the entry in the second row and third column is 2, meaning the weight of the link from node **B** to node **C** is 2. What kind of network does this matrix represent?

**a.** Undirected, unweighted

**b.** Undirected, weighted

**c.** Directed, unweighted

**d.** Directed, weighted

Why?

### Q3 (3 points)

Consider the simple (undirected) network represented by the following graph:

<img src="hw1_plot.png" alt="Simple (undirected) network for hw1 Q3" height="200"><br/>

**a.** Show the degree of each node and make a plot of its (normalized) **degree distribution**.

**b.** Calculate by hand: the diameter and the average path length of the network

**c.** Calculate by hand: the local clustering coefficient of each node and the average local clustering coefficient of the entire network.

### Q4 (1 point)

Consider the network defined by the adjacency matrix in Q2. How many nodes are in this network? How many links? Are there any self-loops?

Discuss how you arrived at your answer.

### Q5 (1 point)

Webflix keeps data on customer preferences using a bipartite network connecting users to movies they have watched and/or rated. Webflix's movie library contains approximately 1,000 movies. In the fourth quarter of 2022, Webflix reported having about 5,000 users. Also, on average, a user has watched and/or rated 750 movies. Approximately how many links are in this network? Would you consider this network sparse or dense? Explain.

## Submission

Make sure that you have committed and pushed your local repo to your private GitHub repo (inside the `hw1` folder).  Your repo should include your report, images, and any code you developed to answer the questions.  Include "Ready to grade @anwala" in your final commit message. 
