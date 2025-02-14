# Readme for the Project
### Versions being used are
- Utilizing ruby 3.2.7 (2025-02-04 revision 02ec315244) [x64-mingw-ucrt]
- MongoDB 8.0
- gem "rails", "~> 8.0.1"
- gem 'mongoid', '~> 8.0'
- gem "puma", ">= 5.0"


  
# Extract/Transform in python

### S3 bucket credentials:
![alt text](images/image-9.png)

### Pull in data using credentials:
![alt text](images/image-10.png)

### This will write/update the csv file:
![alt text](images/image-11.png)

### Final output of Python w/o Ruby
![alt text](images/image-7.png)

### Where the final value being return is made with this part of the code:
![alt text](images/image-8.png)

### Then the final CSV is here, which can be turned into json/xls/etc.
### Note: That once the Ruby Project is complete this section may change
![alt text](images/image-13.png)





# Ruby project located in inventory_api folder of project:

## Inventory API Important files are:

### - inventory_api/Gemfile
![alt text](images/image-4.png)

### - inventory_api/app/controllers/inventory_uploads_controller.rb
![alt text](images/image-6.png)

### inventory_api/app/models/inventory_unit.rb
![alt text](images/image-5.png)





# After setting up Mongodb/Ruby 
### Type rails server
![alt text](images/image-1.png)

### Then you should be able to find server at listen location:
![alt text](images/image-2.png)

### Then setup the Post/Get Command and the model & controller will output the data here 
![alt text](images/image-3.png)



# Last step integrate python 

### Create a generate(), upload(), list_uploads(), and main() script, then run each as an action of main() below:
![alt text](images/image-14.png)


### Kill the ruby/mongodb instances after complete
![alt text](images/image-15.png)
