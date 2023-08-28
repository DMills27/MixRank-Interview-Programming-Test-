

Another edge cases results from a site such as [biznessapps.com](biznessapps) is that it contains a number of assets with "logo" in its metadata. This would have to be pruned with more refined techniques such as perceptual hashing where could compare the images embedding on a given page with the favicon and see if the same hash is generated. An alternative approach would be to use entropy estimation with the objects under study being the same as described in the sentence.

Sites such as facebook and youtube which use .svgs that are embedded in the html and thus not necessary for them to be saved as a separate asset. 

To accomodate greater requests one could use a combination of concurrency and caching with a data store such as Redis.

In order to add concurrency to the solution outlined `base_crawler.py`:
- We would first define a Queue that would store the URLs that want to crawl for the logos.
- Then define a Worker Function which represents the work task for each thread. These would take URLs from the queue, send requests and extract the logo URLs/URIs from these requests that are then added back to the Queue; this is our `get_contents_from_url()` function. 
- We then have to create threads that will create a pool of workers to execute the function correctly. Then start the threads to begin the URLs in the queue.
- We need to stategies to manage concurrency, such as using thread safe structures like locks to prevent race conditions when accessing shared resources. Additionally, one needs to ensure that relevant functions being called adhere to concepts such as purity and [https://softwareengineering.stackexchange.com/a/254306](referential transparency). 
- Finally we need to deal with various issues that may crop up such as overwhemling the servers and getting banned, as well as, an exit strategy for the crawling process. One could use timers and/or rate limiting libraries for this. Much of the error handling is already dealt with in the `get_contents_from_url()` function.