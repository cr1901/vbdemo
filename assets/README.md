By convention, assets do not include the headers in which they are defined to for the following reasons:
* Reduce redundant file inclusion.
* Permit headers which expose that the assets exist (via extern) to vary without needing to update the C files that actually define the assets.

I put this README here in case the differences trip up anyone viewing the source tree- extra comments can't hurt :).
