# Readme for the Project

# Extract/Transform in python

### S3 bucket credentials, also build s3 URL 
![alt text](images/image-9.png)

### Pull in data using credentials
![alt text](images/image-10.png)

### This will write/update the csv file here:
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

# after setting up Mongodb/Ruby 
### Type rails server
![alt text](images/image-1.png)

### Then you should be able to find server at listen location:
![alt text](images/image-2.png)

### Then setup the Post/Get Command and the model & controller will output the data here 
![alt text](images/image-3.png)

# Last step integrate python 

### Create the three scripts, then run each as an action below:
![alt text](images/image-14.png)


### Kill the ruby/mongodb instances
![alt text](images/image-15.png)