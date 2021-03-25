## Face detection and masking pipeline


### Exceptions

Here is the list of exceptions thrown by the face detection and masking pipeline.

| Exception       | Message        | Status code  | Description |
|:------------- |:-------------|:-----| :-----|
| InvalidFaceImage | Please make sure your image has neutral facial expression. | 400 | When face expression in not neutral (like smiling, crying etc) |
| InvalidFaceImage | Please make sure your image is well-lit. | 400 | When the image is dark |
| InvalidFaceImage | Please make sure your image is clear. | 400 | When image is blurry or noisy |
| InvalidFaceImage | Please face straight towards your camera, avoid tiliting. | 400 | When face is not straight upright |
| InvalidFaceImage | Please ensure exactly ONE face is in the image. | 400 | When there is not exactly ONE face in the image |
| InvalidFaceImage | Please ensure your full face is visible in the image, including both ears. | 400 | When face attributes are partially covered |