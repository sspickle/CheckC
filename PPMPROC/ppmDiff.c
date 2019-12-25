/*
HW 10 ppm comparer
Steve Spicklemire
Dec 11, 2019
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

int scanImageData(ImagePPM *anImage, FILE *f) {

    int row = 0;
    int col = 0;
    int pixVal = 0;
    
    fscanf(f, "%s", anImage->magic);
    fscanf(f, "%d", &(anImage->width));
    fscanf(f, "%d", &(anImage->height));
    fscanf(f, "%d", &(anImage->max_value));
    
    anImage->pixels = (Pixel *)malloc(sizeof(Pixel)*anImage->width*anImage->height);

    if (!anImage->pixels) {
      printf("Ack! No memory I guess.\n");
      return 0;
    }

    Pixel *p = anImage->pixels;

    for (row = 0; row < anImage->height; row++) {
        for (col = 0; col < anImage->width; col++) {
            fscanf(f, "%d", &pixVal); // scan in red
            p->red = pixVal;
            fscanf(f, "%d", &pixVal); // scan in green
            p->green = pixVal;
            fscanf(f, "%d", &pixVal); // scan in blue
            p->blue = pixVal;
            p++;
        }
    }
    
    return 1;
}

int pixDiff(Pixel *pA, Pixel *pB, int maxdiff) {
    
    if (abs(pA->red - pB->red) > maxdiff) {
        return 1;
    } else if (abs(pA->green - pB->green) > maxdiff) {
        return 1;
    } else if (abs(pA->blue - pB->blue) > maxdiff) {
        return 1;
    }
    return 0;
}

int diffImages(ImagePPM *imageA, ImagePPM *imageB, int maxdiff) {
    
    int row = 0;
    int col = 0;
    
    if ((imageA->width != imageB->width) || (imageA->height != imageB->height)) {
        return 1;
    }
    
    Pixel *pA = imageA->pixels;
    Pixel *pB = imageB->pixels;
    
    for (row = 0; row < imageA->height; row++) {
        for (col = 0; col < imageA->width; col++) {
            if (pixDiff(pA, pB, maxdiff)) {
                return 1;
            }
            pA++;
            pB++;
        }
    }
    return 0;
}

int main(int argc, char *argv[]) {
    
    ImagePPM imageA; // allocated on the stack
    ImagePPM imageB; // 
    
    if (argc<4) {
        printf("Usage: %s fname1 fname2 maxdiff\n", argv[0]);
        return 1;
    }

    FILE *fileA = fopen(argv[1], "r");
    FILE *fileB = fopen(argv[2], "r");
    int maxdiff = atoi(argv[3]);

    if (!scanImageData(&imageA, fileA)) {
        return -1;
    }
    
    if (!scanImageData(&imageB, fileB)) {
        return 1;
    }
    
    if (diffImages(&imageA, &imageB, maxdiff)) {
        printf("Images are DIFFERENT.\n");
    } else {
        printf("Images compare OK.\n");
    }
    
    free(imageA.pixels);
    imageA.pixels = NULL;
    free(imageB.pixels);
    imageB.pixels = NULL;
    return 0;
}
