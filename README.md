# User Complaints Classification

This is an NLP-based problem solving approach fot the dataset available as a consumer-complaint database for the Banking sector.

https://user-complaints.herokuapp.com/

## User Complaints Classification Project

The ```app``` folder contains services, static and templates. This is for flask. Also contains app.py used to run the application.
The rest of the project are structured like:

<img src="https://github.com/luanagbmartins/user-complaints/blob/master/organization.png" width="550" height="550">

## Instructions

To run locally go to ```app``` folder and run ```python manage.py runserver```. 
To training models run ```train_model``` script.

## Examples

For the input

```I have a personal loan from Patriot finance. They are incorrectly reporting that my loan is a derogatory status and showing as many days late. We have a payment agreement and I am paying as agreed and my account does not reflect this.```

we have this results:

![complaint-1](https://github.com/luanagbmartins/user-complaints/blob/master/reports/figures/complaint-portal_1.png)
![complaint-2](https://github.com/luanagbmartins/user-complaints/blob/master/reports/figures/complaint-portal_2.png)
