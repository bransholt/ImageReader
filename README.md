# ImageReader - OCR (Object Character Recognition) for PDF Reading Automation

Object Character Recognition (OCR) implemented with Google's Tesseract. This program utilizes Google's OCR application to read text directly from images. The purpose of this project is to retrieve key information from images or pdfs and to then organize this information into an exel file for later use. This program is ideal for pdf automation by those who see a high volume of pdf data and spend most of their time reading/typing out this information. This program is tailored toward one specific example but can be easily tailored for your own personal use.

## Getting Started

The peice that holds this program together and makes it work is Google's Pytesseract. In order to get Pytesseract working on your machine, you must first download it to your system.

[Pytesseract Download Page](https://pypi.org/project/pytesseract/#files)

In the ImageReader.py file, you must change the string in line 15 to have your username in the "/USER/" part of the string. Keep in mind that this filepath is where Tesseract is typically downloaded too, but that might not be the case for you. Make sure that you have found the location of this filepath. Without completing this step, this code will not work.

After you have installed tesseract, you must install all of the dependencies listed in the requirements.txt file in the main directory. In order for this program to work you must have these dependencies installed.

## Installing Dependencies

Inside the requirements.txt is a list of 3 packages required for this program to run. Insalling these dependencies is as simple as typing

>pip install -r requirements.txt

Make sure that you are in the ImageReader directory when typing in this command.

## How to run your ImageReader

The queue is where files that need to be processed go. Whether you are processing pdfs or images (.png, .jpeg, etc.) you will place them here. Once you run ImageReader.py, all original pdfs will be moved to the original_pdfs directory and a jpg copy of the pdf will be produced in queue. Once all the images have been processed they are moved to the processed_images directory. If you try to run ImageReader.py with files that have the same name, you will recieve an error (so make sure that all files have unique names). Once the pdfs have been converted into images, the system will create a sub-directory in the output directory with the name of the folder being the current date and time. This is so folder with the same name can be produced, and so that you can document when you last ran ImageReader.

The resulting output will be stored in the dated folder as a csv file with all of your entries into it. Every time you run this program, it will create a new csv and store that in the folder created during processing. This means that this program does not append new entries into already existing csvs. This can be changed easily though if that is what you want. 



## General Purpose

This application was written to be easily modified for many automation purposes. In this example we are using it to read and store specific data to a csv file, but by editing the "wrangle_cert" method, you can extract any text you want from any standardized set of images you want. With that being said, this program makes a great foundation for any of your PDf reading tasks.
