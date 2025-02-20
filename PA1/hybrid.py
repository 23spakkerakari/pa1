import numpy as np

def cross_correlation_2d(img, kernel):
    '''Given a kernel of arbitrary m x n dimensions, with both m and n being
    odd, compute the cross correlation of the given image with the given
    kernel, such that the output is of the same dimensions as the image and that
    you assume the pixels out of the bounds of the image to be zero. Note that
    you need to apply the kernel to each channel separately, if the given image
    is an RGB image.

    Inputs:
        img:    Either an RGB image (height x width x 3) or a grayscale image
                (height x width) as a numpy array.
        kernel: A 2D numpy array (m x n), with m and n both odd (but may not be
                equal).

    Output:
        Return an image of the same dimensions as the input image (same width,
        height and the number of color channels)
    '''
    # TODO-BLOCK-BEGIN

    kernel_height, kernel_width = kernel.shape
    pad_h, pad_w = kernel_height // 2, kernel_width // 2

    # grayscale images
    if img.ndim == 2:
        h, w = img.shape
        padded_img = np.pad(img, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=0)
        output = np.zeros((h, w))

        # apply kernel over image
        for i in range(h):
            for j in range(w):
                region = padded_img[i: i + kernel_height, j:j + kernel_width]
                output[i, j] = np.sum(region * kernel)
        return output 
    # rgb images
    elif img.ndim == 3:
        h, w, channels = img.shape
        output = np.zeros((h, w, channels))

        for c in range(channels):
            # get zero-padded image of current color channel
            padded_img = np.pad(img[:, :, c], ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=0)
            # apply kernel over image for channel
            for i in range(h):
                for j in range(w):
                    region = padded_img[i: i + kernel_height, j:j + kernel_width]
                    output[i, j, c] = np.sum(region * kernel)
        return output 
    else: 
        raise Exception("You gave us an interesting image dimension! The image input has to be either in grayscale or color")


    ## Now we consider whether the image is grayscale (ndimension is 2) or if its color (ndimension is 3)


    # raise Exception("TODO in hybrid.py not implemented")
    # TODO-BLOCK-END

def convolve_2d(img, kernel):
    '''Use cross_correlation_2d() to carry out a 2D convolution.

    Inputs:
        img:    Either an RGB image (height x width x 3) or a grayscale image
                (height x width) as a numpy array.
        kernel: A 2D numpy array (m x n), with m and n both odd (but may not be
                equal).

    Output:
        Return an image of the same dimensions as the input image (same width,
        height and the number of color channels)
    '''
    # TODO-BLOCK-BEGIN
    # raise Exception("TODO in hybrid.py not implemented")
    
    flipped_kernel = kernel[::-1, ::-1]
    return cross_correlation_2d(img, flipped_kernel)

    # TODO-BLOCK-END

def gaussian_blur_kernel_2d(sigma, height, width):
    '''Return a Gaussian blur kernel of the given dimensions and with the given
    sigma. Note that width and height are different.

    Input:
        sigma:  The parameter that controls the radius of the Gaussian blur.
                Note that, in our case, it is a circular Gaussian (symmetric
                across height and width).
        width:  The width of the kernel.
        height: The height of the kernel.

    Output:
        Return a kernel of dimensions height x width such that convolving it
        with an image results in a Gaussian-blurred image.
    '''

    # TODO-BLOCK-BEGIN

    y = np.arange(height) - (height - 1) / 2.0
    x = np.arange(width) - (width - 1) / 2.0
    x, y = np.meshgrid(x, y)
    # raise Exception("TODO in hybrid.py not implemented")

    # calculate kernel with gaussian
    kernel = np.exp(-(x**2 + y**2) / (2 * sigma ** 2))

    # normalize
    kernel /= np.sum(kernel)

    return kernel
    # TODO-BLOCK-END

def low_pass(img, sigma, size):
    '''Filter the image as if its filtered with a low pass filter of the given
    sigma and a square kernel of the given size. A low pass filter supresses
    the higher frequency components (finer details) of the image.

    Output:
        Return an image of the same dimensions as the input image (same width,
        height and the number of color channels)
    '''
    # TODO-BLOCK-BEGIN

    kernel = gaussian_blur_kernel_2d(sigma, size, size)

    return convolve_2d(img, kernel)
    # raise Exception("TODO in hybrid.py not implemented")
    # TODO-BLOCK-END

def high_pass(img, sigma, size):
    '''Filter the image as if its filtered with a high pass filter of the given
    sigma and a square kernel of the given size. A high pass filter suppresses
    the lower frequency components (coarse details) of the image.

    Output:
        Return an image of the same dimensions as the input image (same width,
        height and the number of color channels)
    '''
    # TODO-BLOCK-BEGIN
    # raise Exception("TODO in hybrid.py not implemented")

    low_pass_img = low_pass(img, sigma, size)
    # Subtract the low-pass image from the original image to isolate high-frequency details.
    high_pass_img = img - low_pass_img
    return high_pass_img
    # TODO-BLOCK-END

def create_hybrid_image(img1, img2, sigma1, size1, high_low1, sigma2, size2,
        high_low2, mixin_ratio, scale_factor):
    '''This function adds two images to create a hybrid image, based on
    parameters specified by the user.'''
    high_low1 = high_low1.lower()
    high_low2 = high_low2.lower()

    if img1.dtype == np.uint8:
        img1 = img1.astype(np.float32) / 255.0
        img2 = img2.astype(np.float32) / 255.0

    if high_low1 == 'low':
        img1 = low_pass(img1, sigma1, size1)
    else:
        img1 = high_pass(img1, sigma1, size1)

    if high_low2 == 'low':
        img2 = low_pass(img2, sigma2, size2)
    else:
        img2 = high_pass(img2, sigma2, size2)

    img1 *=  (1 - mixin_ratio)
    img2 *= mixin_ratio
    hybrid_img = (img1 + img2) * scale_factor
    return (hybrid_img * 255).clip(0, 255).astype(np.uint8)

