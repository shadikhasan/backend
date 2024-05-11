from django.db import models
from waste_management.models import Area, SecondaryTransferStation


class ThirdPartyContractor(models.Model):
    name = models.CharField(max_length=100)
    contract_id = models.CharField(max_length=50, unique=True)
    reg_id = models.CharField(max_length=50)
    reg_date = models.DateField(auto_now=True)
    tin = models.CharField(max_length=20)
    contact_number = models.CharField(max_length=20)
    workforce_size = models.PositiveIntegerField()
    payment_per_ton = models.DecimalField(max_digits=10, decimal_places=2)
    waste_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    contract_duration = models.DurationField()
    area_of_collection = models.ForeignKey(Area, related_name='collection_contractors', on_delete=models.CASCADE)
    designated_sts = models.ForeignKey(SecondaryTransferStation, related_name='sts_contractors', on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.name

class Employee(models.Model):
    employee_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    date_of_hire = models.DateField()
    job_title = models.CharField(max_length=100)
    payment_rate_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    contact_information = models.CharField(max_length=100)
    assigned_collection_route = models.CharField(max_length=100)
    
    def __str__(self):
        return self.full_name
    
    
class LoggedWorkingHours(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    login_time = models.DateTimeField()
    logout_time = models.DateTimeField(blank=True, null = True)
    total_hours_worked = models.DecimalField(max_digits=5, decimal_places=2, default = 0, editable = False)
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2, default = 0, editable = False)
    absences_and_leaves = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.employee.full_name} - {self.login_time.date()}"
    
    def save(self, *args, **kwargs):
        if self.login_time and self.logout_time:
            time_difference = self.logout_time - self.login_time
            total_hours = time_difference.total_seconds() / 3600  # convert seconds to hours
            if total_hours > 8:  # assuming 8 hours is regular working time
                self.total_hours_worked = 8
                self.overtime_hours = total_hours - 8
            else:
                self.total_hours_worked = total_hours
                self.overtime_hours = 0
        super().save(*args, **kwargs)


class WasteCollection(models.Model):
    WASTE_TYPES = [
        ('domestic', 'Domestic Waste'),
        ('plastic', 'Plastic Waste'),
        ('construction', 'Construction Waste'),
        # Add more choices as needed
    ]
    
    datetime_of_collection = models.DateTimeField()
    waste_amount_kg = models.DecimalField(max_digits=10, decimal_places=2)
    contractor = models.ForeignKey(ThirdPartyContractor, on_delete=models.CASCADE)
    waste_type = models.CharField(max_length=100, choices=WASTE_TYPES)
    designated_sts = models.ForeignKey(SecondaryTransferStation, on_delete=models.CASCADE)
    vehicle_used = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.datetime_of_collection} - {self.contractor}"
    
    

class Billing(models.Model):
    contractor = models.ForeignKey(ThirdPartyContractor, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    basic_pay = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    deficit = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    fine = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable = False)
    total_bill = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    collected_waste = models.DecimalField(max_digits=10, decimal_places=3)
    def __str__(self):
        return f"Billing for {self.contractor} on {self.date}"

    def save(self, *args, **kwargs):
        # Calculate basic pay
        self.basic_pay = self.contractor.payment_per_ton * self.collected_waste
        
        # Determine deficit
        self.deficit = max(0, self.contractor.waste_per_day - self.collected_waste)
        
        # Calculate fine
        self.fine = self.deficit * self.contractor.designated_sts.fine_for_compensation
        #print(str(self.deficit)  + " " + str(self.contractor.designated_sts.fine_for_compensation))
        # Calculate total bill
        self.total_bill = self.basic_pay - self.fine
        
        super().save(*args, **kwargs)