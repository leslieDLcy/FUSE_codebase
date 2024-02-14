## Loads onto the elements

For the wind load, we have considered (i) distributed loads on the elements and (ii) concentrated load (nodal force) at the hub height.

There shall be 15 load series (distributed load $f$) for the tower and one load $F$ for the upper node at the hub height. The implementation can be found in [Wind scenario](wind_scenarios.ipynb).

Besides, a stochastic model (i.e. Kaimal model) listed in the IEC code (B.14) has also been implemented. Refer to [Kaimal implementation](Kaimal_implementation.ipynb).

In addition, the file [Wind load 101](wind_loading101.ipynb) illustrates all the wind velocity and turbulence models set out in the IEC code. These models can all be implemented if we want. Currently we are focusing on scenario 6.2 as recommended by SSE.

The rest of codes are library codes.



