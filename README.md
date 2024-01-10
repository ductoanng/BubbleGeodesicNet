# BubbleGeodesicNet
This program contructs geodesic net inspired from Steiner Tree problem. The algorithm tries to mimic the process of building the Steiner tree with a soap bubble film. We can see that process from this video https://www.youtube.com/watch?v=BVbIRM01UTs.

This algorithm starts from constructing a minimum spanning tree on a given set of points. Then, it modifies the tree by adding new balanced points (or Steiner points) using Fermat-Torricelli point of a triangle. It also rearranges the edges connecting those points to minimize the total length. 

### Instruction:
You can try the algorithm by running the file **mst-bubble.py**. You can modify the list of unbalanced points (input).

### Goal: 
We desire to construct that type of network in other high-dimension surfaces such as sphere or torus.

### References:
- Geodesit Net: https://doi.org/10.1080/10586458.2020.1743216
- Fermat-Torricelli point: https://mathworld.wolfram.com/FermatPoints.html
- Steiner Tree: https://en.wikipedia.org/wiki/Steiner_tree_problem
