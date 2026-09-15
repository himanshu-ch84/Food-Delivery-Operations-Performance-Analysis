import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('food_delivery_cleaned.csv')

df['order_date'] = pd.to_datetime(
    df['order_date'],
    errors='coerce'
)

df['time_orderd'] = pd.to_datetime(
    df['time_orderd'],
    format='mixed',
    errors='coerce'
)
                            

df['time_order_picked'] = pd.to_datetime(
    df['time_order_picked'],
    format='mixed',
    errors='coerce'
)
                      

print(df.dtypes)
print(df[['order_date', 'time_orderd', 'time_order_picked']].isna().sum())

#Analysis:
 
# Q1. What is the distribution of delivery time?
plt.hist(df['time_taken_min'], bins = 20, color = 'red', edgecolor = 'black')
plt.xlabel('Time Taken (minutes)')
plt.ylabel('no. of orders')
plt.title('Distribution of Time Taken for Delivery')
plt.show()

# # Q2.How does delivery time vary by traffic density?
avg_delivery_time = df.groupby('road_traffic_density')['time_taken_min'].mean()

plt.bar(avg_delivery_time.index, avg_delivery_time.values, color = 'blue')
plt.bar_label(plt.bar(avg_delivery_time.index, avg_delivery_time.values, color = 'blue'), fmt='%.2f')
plt.xlabel('Road Traffic Density')
plt.ylabel('Average Delivery Time (minutes)')
plt.title('Delivery Time by Traffic Density')
plt.show()

# # Q3. How does weather affect delivery time?
avg_delivery_time_by_weather = df.groupby('weather_conditions')['time_taken_min'].mean()

plt.bar(avg_delivery_time_by_weather.index, avg_delivery_time_by_weather.values, color = 'green')
plt.bar_label(plt.bar(avg_delivery_time_by_weather.index, avg_delivery_time_by_weather.values, color = 'green'), fmt = '%.2f')
plt.xlabel('Weather Conditions')
plt.ylabel('Average Delivery Time (minutes)')
plt.title('Delivery Time by Weather Conditions')
plt.show()

# # Q4. How do multiple deliveries affect delivery time?
avg_delivery_time_by_multiple_deliveries = df.groupby('multiple_deliveries')['time_taken_min'].mean()

plt.bar(avg_delivery_time_by_multiple_deliveries.index, avg_delivery_time_by_multiple_deliveries.values, color= 'orange')
plt.bar_label(plt.bar(avg_delivery_time_by_multiple_deliveries.index, avg_delivery_time_by_multiple_deliveries.values, color= 'orange'), fmt= '%.2f')
plt.xlabel('Multiple Deliveries')
plt.ylabel('Average Delivery Time (minutes)')
plt.title('Delivery Time by Multiple Deliveries')
plt.show()

# # Q5. How does delivery time vary by vehicle type?
avg_delivery_time_by_vehicle_type = df.groupby('type_of_vehicle')['time_taken_min'].mean()

plt.bar(avg_delivery_time_by_vehicle_type.index, avg_delivery_time_by_vehicle_type.values, color = 'purple')
plt.bar_label(plt.bar(avg_delivery_time_by_vehicle_type.index, avg_delivery_time_by_vehicle_type.values, color = 'purple'), fmt = '%.2f')
plt.xlabel('Type of Vehicle')
plt.ylabel('Average Delivery Time (minutes)')
plt.title('Delivery Time by Vehicle Type')
plt.show()

# # Q6. How does delivery time vary by city?
avg_delivery_time_by_city = df.groupby('city')['time_taken_min'].mean()

plt.bar(avg_delivery_time_by_city.index, avg_delivery_time_by_city.values, color = 'brown')
plt.bar_label(plt.bar(avg_delivery_time_by_city.index, avg_delivery_time_by_city.values, color = 'brown'), fmt = '%.2f')
plt.xlabel('City')
plt.ylabel('Average Delivery Time (minutes)')
plt.title('Delivery Time by City')
plt.show()

# Q7. How does delivery time vary by delivery-person rating?
avg_delivery_time_by_delivery_person_rating = df.groupby('delivery_person_ratings')['time_taken_min'].mean()

plt.plot(avg_delivery_time_by_delivery_person_rating.index, avg_delivery_time_by_delivery_person_rating.values, color = 'pink', marker = 'o')
plt.xlabel('Delivery Person Rating')
plt.ylabel('Average Delivery Time (minutes)')
plt.title('Delivery Time by Delivery Person Rating')
plt.show()

# Q8. How does delivery time vary by festival status?
avg_delivery_time_by_festival = df.groupby('festival')['time_taken_min'].mean()

plt.bar(avg_delivery_time_by_festival.index, avg_delivery_time_by_festival.values, color = 'cyan')
plt.bar_label(plt.bar(avg_delivery_time_by_festival.index, avg_delivery_time_by_festival.values, color = 'cyan'), fmt = '%.2f')
plt.xlabel('Festival Status')
plt.ylabel('Average Delivery Time (minutes)')
plt.title('Delivery Time by Festival Status')
plt.show()

# Q9. How does delivery time vary by order hour?
df['order_hour'] = df['time_orderd'].dt.hour
avg_delivery_time_by_order_hour = df.groupby('order_hour')['time_taken_min'].mean()

plt.plot(avg_delivery_time_by_order_hour.index, avg_delivery_time_by_order_hour.values, color = 'magenta', marker = 'o')
plt.xlabel('Order Hour')
plt.ylabel('Average Delivery Time (minutes)')
plt.title('Delivery Time by Order Hour')
plt.show()