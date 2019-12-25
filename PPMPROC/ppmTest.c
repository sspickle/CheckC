/*
HW 10 solution
Steve Spicklemire
Nov 25, 2019
*/

/*
Program to perform simple image processing steps:

1) Black Level: specify a certain luminosity level is to be
    translated to “black”. All pixel RGB values are scaled according
    to this new black-level.

2) Auto-Black Level: use the pixel with the minimum luminosity as the
    “new black” and adjust all other pixels accordingly.

3) White Level: specify a certain luminosity level is to be
    translated to “white”. All pixel RGB values are scaled according
    to this new white-level.

4) Auto-White Level: use the pixel value with a maximum luminosity as
    the “new white” and scale all the other pixels accordingly.

5) Auto-Contrast: This is effectively the combination of option (2)
    and (4) simultaneously. The min-luminosity becomes the new black,
    and max-luminosity becomes white.

*/

#include <stdio.h>
#include <stdlib.h>

typedef struct _pixel {
    int red;
    int green;
    int blue;
} Pixel;

typedef struct _imagePPM {
    char magic[3];  // magic identifier, "P3" for PPM
    int width;      // number of columns
    int height;     // number of rows
    int max_value;  // maximum intensity of RGB components
    Pixel *pixels;  // the actual color pixel data 
} ImagePPM;

int scanImageData(ImagePPM *anImage) {

    int row = 0;
    int col = 0;
    int pixVal = 0;
    
    scanf("%s", anImage->magic);
    scanf("%d", &(anImage->width));
    scanf("%d", &(anImage->height));
    scanf("%d", &(anImage->max_value));
    
    anImage->pixels = (Pixel *)malloc(sizeof(Pixel)*anImage->width*anImage->height);

    if (!anImage->pixels) {
      printf("Ack! No memory I guess.\n");
      return 0;
    }

    Pixel *p = anImage->pixels;

    for (row = 0; row < anImage->height; row++) {
        for (col = 0; col < anImage->width; col++) {
            scanf("%d", &pixVal); // scan in red
            p->red = pixVal;
            scanf("%d", &pixVal); // scan in green
            p->green = pixVal;
            scanf("%d", &pixVal); // scan in blue
            p->blue = pixVal;
            p++;
        }
    }
    
    return 1;
}

void printImageData(ImagePPM *anImage) {
    int row = 0;
    int col = 0;
    Pixel *p = anImage->pixels;

    printf("P3\n");
    printf("%d %d %d\n", anImage->width, anImage->height, anImage->max_value);
    
    for (row = 0; row < anImage->height; row++) {
        for (col = 0; col < anImage->width; col++) {
            printf("%d %d %d \n", p->red, p->green, p->blue);
            p++;
        }
    }
}

double luminosity(Pixel *p) {
    return 0.2126*p->red + 0.7152*p->green + 0.0722*p->blue;
}

double findMaxLuminosity(ImagePPM *anImage){
    /*
    Step through the image pixels and find the max luminosity.
    */
    Pixel *p = anImage->pixels;
    int row = 0;
    int col = 0;
    double maxLum = luminosity(p);
    double currLum = maxLum;

    for (row = 0; row < anImage->height; row++) {
        for (col = 0; col < anImage->width; col++) {
            currLum = luminosity(p);
            if (currLum > maxLum) {
                 maxLum = currLum;
            }
            p++;
        }
    }
    return maxLum;
}

double findMinLuminosity(ImagePPM *anImage){
    /*
    Step through the image pixels and find the min luminosity.
    */

    Pixel *p = anImage->pixels;
    int row = 0;
    int col = 0;
    double minLum = luminosity(p);
    double currLum = minLum;

    for (row = 0; row < anImage->height; row++) {
        for (col = 0; col < anImage->width; col++) {
            currLum = luminosity(p);
            if (currLum < minLum) {
                 minLum = currLum;
            }
            p++;
        }
    }
    return minLum;
}

int newBlackLevel(int currVal, int maxVal, int newBlack) {
    /*
    Compute the new black level of a color component based
    on the current value of of the color component and
    the new desired black value.
    */
    
    double newVal = (double)(currVal - newBlack)/(maxVal - newBlack)*maxVal;
    if (newVal < 0.0) {
        newVal = 0.0;
    }
    return (int)(newVal + 0.50); // round up!
}

int newWhiteLevel(int currVal, int maxVal, int newWhite) {
    /*
    Compute the new white level of a color component based
    on the current value of of the color component and
    the new desired white value.
    */
    double newVal = (double)(currVal)/newWhite*maxVal;
    if (newVal > maxVal) {
        newVal = maxVal;
    }
    return (int)(newVal + 0.50); // round up!
}

void resetImageBlackLevel(ImagePPM *anImage, int newBlack) {
    /*
    ** step through all the pixels resetting the black level
    */
    
    Pixel *p = anImage->pixels;
    int row = 0;
    int col = 0;

    for (row = 0; row < anImage->height; row++) {
        for (col = 0; col < anImage->width; col++) {
            p->red = newBlackLevel(p->red, anImage->max_value, newBlack);
            p->green = newBlackLevel(p->green, anImage->max_value, newBlack);
            p->blue = newBlackLevel(p->blue, anImage->max_value, newBlack);
            p++;
        }
    }
}

void resetImageWhiteLevel(ImagePPM *anImage, int newWhite) {
    /*
    ** step through all the pixels resetting the black level
    */
    
    Pixel *p = anImage->pixels;
    int row = 0;
    int col = 0;

    for (row = 0; row < anImage->height; row++) {
        for (col = 0; col < anImage->width; col++) {
            p->red = newWhiteLevel(p->red, anImage->max_value, newWhite);
            p->green = newWhiteLevel(p->green, anImage->max_value, newWhite);
            p->blue = newWhiteLevel(p->blue, anImage->max_value, newWhite);
            p++;
        }
    }
}

void autoWhiteLevel(ImagePPM *anImage) {
    resetImageWhiteLevel(anImage, (int)findMaxLuminosity(anImage));
}

void autoBlackLevel(ImagePPM *anImage) {
    resetImageBlackLevel(anImage, (int)findMinLuminosity(anImage));
}

void autoContrast(ImagePPM *anImage) {
    autoWhiteLevel(anImage);
    autoBlackLevel(anImage);
}

int main(int argc, char *argv[]) {
    
    ImagePPM myImage; // allocated on the stack this limits max image size!
    if (!scanImageData(&myImage)) {
        return -1;
    }
    
    if (argc<2) {
        printf("Ack! I need more arguments.\n");
    } else {
        int operation = atoi(argv[1]);
        switch(operation) {
            case 1:
                if (argc < 3) {
                    printf("Ack! I need a black level\n");
                    break;
                }
                int newBlack = atoi(argv[2]);
                resetImageBlackLevel(&myImage, newBlack);
                printImageData(&myImage);
                break;

            case 2:
                autoBlackLevel(&myImage);
                printImageData(&myImage);
                break;
            
            case 3:
                if (argc < 3) {
                    printf("Ack! I need a white level\n");
                    break;
                }
                int newWhite = atoi(argv[2]);
                resetImageWhiteLevel(&myImage, newWhite);
                printImageData(&myImage);
                break;

            case 4:
                autoWhiteLevel(&myImage);
                printImageData(&myImage);
                break;
                
            case 5:
                autoContrast(&myImage);
                printImageData(&myImage);
                break;
                
            case 6:
                printf("Max Lum: %5.2f\n", findMaxLuminosity(&myImage));
                break;

            case 7:
                printf("Min Lum: %5.2f\n", findMinLuminosity(&myImage));
                break;

            default:
                printf("Ack! Invalid input option\n");
        }
    }
    
    free(myImage.pixels);
    myImage.pixels = NULL;

    return 0;
}
