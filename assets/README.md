By convention, assets do not include the headers in which they are defined to for reasons:
*Reduce redundant file inclusion.
*Permit headers which expose that the assets exist (via extern) to vary without needing to update the C files that actually define the assets.

