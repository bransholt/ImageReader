## this file is soley for trying to convert our program for reading pdfs and putting the requested data into an exel sheet
#necessary Imports
import os
import sys
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from os import path
import shutil
from datetime import datetime
import csv

#find the file path for pytesseract and put it here. Typically is installed in this location for windows users. Put your 
#user name in the USER space
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe'


class ImageReader:
    
    def __init__(self):
        return None
    
    
    #DONE
    def retrieve_filenames(self):
        fp = '../data/queue/'
        filepaths = {}
        files_in_queue = os.listdir(fp)
        images_to_process = []
        pdfs_to_convert = []
        for file in files_in_queue:
            if file.lower().endswith(('.png', '.jpg', 'jpeg')):
                images_to_process.append(fp+file)
            elif file.lower().endswith('pdf'):
                pdfs_to_convert.append(fp+file)
        filepaths['0'] = images_to_process
        filepaths['1'] = pdfs_to_convert
        return filepaths
            
            
            
            
    def convert_pdf_to_image(self, filename):
        fp = '../data/queue/'
        print("File conversion started (pdf to image): " + filename)
        # Store all the pages of the PDF in a variable 
        pages = convert_from_path(filename, 500) 
  
        # Counter to store images of each page of PDF to image 
        image_counter = 1
        filename_temp = filename[:len(filename)-4]
        
  
        # Iterate through all the pages stored above 
        for page in pages: 
  
            # Declaring filename for each page of PDF as JPG 
            # For each page, filename will be: 
            # PDF page 1 -> page_1.jpg 
            # PDF page 2 -> page_2.jpg 
            # PDF page 3 -> page_3.jpg 
            # .... 
            # PDF page n -> page_n.jpg 
            new_filename = filename_temp+"_"+str(image_counter)+".jpg"
      
            # Save the image of the page in system 
            page.save(new_filename, 'JPEG') 
  
            # Increment the counter to update filename 
            image_counter = image_counter + 1

        if path.exists(filename):
            shutil.move(filename, "../data/original_pdfs/")
        print("File Conversion ended (pdf to image) Resulting Image: " + new_filename + "\n")
        return new_filename
    
    
    def read_image(self, filename, output_dir):
        #this method is for extracting the text from the specified image file
        #this is a general method and will work for any use case. The calling
        #of wrangle_cert is specific to my problem but can be edited for your own use case.
        
        output_dir = output_dir
        #this line of code (pytesseract) is what does the job of reading the text from the images
        text = str(((pytesseract.image_to_string(Image.open(filename)))))
        self.wrangle_cert(text, output_dir)
        
        #move the images that have been processed to processed_images directory
        shutil.move(filename, '../data/processed_images/')
    
    
    def wrangle_cert(self, text, destination):
        #this is the method that you need to modify for your own use case.
        #all this method does is take the text that is extraced and wrangles it to get the information that we want
        
        text = text.lower()
        text = text.replace('-\n', '')
        text = text.replace('\n', ' ')
        #print(text)
        name_low = text.find('certifies that')
        name_up = text.find('has successfully')
        name = text[name_low+len('certifies that'):name_up].strip()
        #print(name)
        course_low = text.find('id:') +3
        course_up = text.find('inst')
        course = text[course_low:course_up].strip().upper()
        #print(course)
        date_low = text.find(' on') +3
        date_up = text.find('(s')
        date = text[date_low:date_up].strip()
        
        name = name.split(' ')
        if len(name) == 2:
            first = name[0].title()
            middle = 'NMM'
            last = name[1].title()
        elif len(name) == 3:
            first = name[0].title()
            middle = name[1].upper()
            last = name[2].title()
        else:
            print("Error: The name that was presented does not have the correct number of parts.")
        
        output_file_name = destination +'/cert_data.csv'
        first_fields = ['First', 'Middle', 'Last', 'CourseID', 'Date']
        fields=[first, middle, last, course, date]
        
        if not path.exists(output_file_name):
            with open(output_file_name, 'w+', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(first_fields)

        with open(output_file_name, 'a', newline='') as u:
            writer = csv.writer(u)
            writer.writerow(fields)
        return output_file_name
        
    def main(self):
        print('------------------Processing Started------------------ \n')
        #fp is the directory where all the images to be processed are
        fp = '../data/queue/'

        files = self.retrieve_filenames()
        #once the filenames (files) are retrieved, the files that need to be converted to images will need to be converted. We
        #check whether there is any items in the dictionary with a key 1. If there is then we will need to take those items (filepaths)
        #and use a for loop to call the convert function and after they are called, verfy that they have been converted and the previous file
        #has been deleted, and once that's done we can move to the next step.
        files_to_be_converted = files['1']
        ok_files = files['0']
        csv_loc = ""
        for file in files_to_be_converted:
            new_filename = self.convert_pdf_to_image(file)
            #this above line will convert the file and delete the old file.
            ok_files.append(new_filename)
        now = datetime.now()
        dt_string = now.strftime("%d_%m_%Y %H_%M_%S")
        output_dir = "../output/"+dt_string
        os.mkdir(output_dir)
        
        print(dt_string + " directory created for output of excel file\n")
        for file in ok_files:
            #takes each file that has been converted to a jpg and starts extracting the text and organizing
            #it to be exported into a csv file.
            self.read_image(file, output_dir)
        print('------------------Processing Finished------------------ \n')
        print(str(len(ok_files)) + " Images Processed")

            
imgrdr = ImageReader()
imgrdr.main()