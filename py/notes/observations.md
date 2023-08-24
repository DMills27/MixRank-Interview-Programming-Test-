

A rudimentary solution presented in .. works by utilising the meta data from various elements such as image, anchor and div tags, and then checking if a src attribute 
shows where a possible logo asset could be found. The edges cases stem from sites which redirect to different URLS, such as sprint.com which redirects to t-mobile.com and biznessapps.com that redirects tobuildfire.com, from which this new website url needs to be noted as it contains the correct path for any logo image. Another edge cases results from a site such as biznessapps.com is that it contains a number of assets with "logo" in its metadata. This would have to be pruned with more refined techniques such as perceptuaal hashing where could compare the images embedding on a given page with the favicon and see if the same hash is generated. An alternative approach would be to use entropy estimation with the objects under study being the same as described in the sentence.

Sites such as facebook and youtbe which use svgs that are embedded in the html and thus not necessary for them to be saved as a separate asset. 

To accodoate greater requests one could use a combination of both concurrency and caching with a data store such as Redis.