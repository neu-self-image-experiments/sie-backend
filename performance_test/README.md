## Performance Testing

This direactory provides a way to test out the performance of the pipeline. It creates a given number of threads. Each thread is going to upload an image to the GCP storage bucket (sie-raw-images). Each thread then wait until a certain file is generated inside another bucket (sie-stimuli-images). Once the image generation is finished, each thread is going to report the start and finish time. The program then take the miniumn start time, and maximum end time. Eventually, it computes the thoughput of the program.

### Running the program

To run the program, you need three parameters:

| Parameters | Description |
|:-----|:-------|
| num_thread | The number of thread that the program will run. |
| file_dir | The directory for all the images waiting to be uploaded. |
| threashold | A threshold to determine whether image processing is finished. |

The following command will run the program:

```
python main.py NUM_THREAD FILE_DIR THREASHOLD
```

### Result

The recent test shows each image is completed in approximately 40 seconds.
