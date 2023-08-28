
## Issues and edge cases
Some edge cases result when a site such as [biznessapps.com](biznessapps) is crawled. The edge case stems from the fact that response body may contain a number of assets with "logo" in its metadata. 
Sites such as facebook and youtube which use `.svgs` that are embedded in the html and thus not necessary for them to be saved as a separate asset. 
This would have to be pruned with more refined techniques such as perceptual hashing where could compare the images embedding on a given page with the favicon and see if the same hash is generated. Perceptual hashing
can be consider an analogue to convenitional hashing
An alternative approach would be to use histogram entropy estimation with the logos under study being the same as described in the sentence. A breif sketch of this method is given as follows:

- Histogram calculation: Calculate the pixel intesities for each image, one can use the formula given [here](https://math.stackexchange.com/a/1019257).
- Normalise the histograms: By dividing the frequency of each intensity value by the total number of pixels in the image. This ensures that the histograms are comparable regardless of image size.
- Entrophy calculation: Calculate the entropy of the normalized histograms. Entropy is a measure of the randomness or uncertainty in a distribution. It is calculated using the formula:
```math
H(x) = -\sum_{i=1}^n p(x_i) \log_2p(x_i)
```
where $p(x_i)$ is the probability of intensity $x_i$ occurring in the histogram, and the sum is taken over all possible intensity values.
- Entropy Comparison: Compare the entropy values of the two images. A lower entropy indicates a more predictable histogram with fewer intensity variations, while a higher entropy suggests a more diverse and varied histogram.
- Similarity Inference: If the entropy values of the two images are close or similar, it indicates that the images have similar distributions of pixel intensities, which suggests visual similarity.
- Define Threshold: Define a threshold value for entropy difference. If the absolute difference between the entropy values of the two images is below this threshold, consider the images as visually similar.

If the entropy values of the two images are close or similar, it indicates that the images have similar distributions of pixel intensities, which suggests visual similarity.

## Using concurrency to achieve better results
To accomodate greater requests one could use a combination of concurrency and caching with a data store such as Redis.

In order to add concurrency to the solution outlined `base_crawler.py`:
- We would first define a Queue that would store the URLs that want to crawl for the logos.
- Then define a Worker Function which represents the work task for each thread. These would take URLs from the queue, send requests and extract the logo URLs/URIs from these requests that are then added back to the Queue; this is our `get_contents_from_url()` function. 
- We then have to create threads that will create a pool of workers to execute the function correctly. Then start the threads to begin the URLs in the queue.
- We need to stategies to manage concurrency, such as using thread safe structures like locks to prevent race conditions when accessing shared resources. Additionally, one needs to ensure that relevant functions being called adhere to concepts such as purity and [https://softwareengineering.stackexchange.com/a/254306](referential transparency). 
- Finally we need to deal with various issues that may crop up such as overwhemling the servers and getting banned, as well as, an exit strategy for the crawling process. One could use timers and/or rate limiting libraries for this. Much of the error handling is already dealt with in the `get_contents_from_url()` function.