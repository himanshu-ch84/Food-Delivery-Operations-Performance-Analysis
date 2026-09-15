import pandas as pd
import numpy as np

df=pd.read_csv('food_delivery.csv')
print(df.head(5))
df.info()
print(df.shape)
df.columns=df.columns.str.strip().str.lower()
df.rename(columns={'time_taken (min)': 'time_taken_min'}, inplace=True)


def convert_time(x):
    if pd.isna(x):
        return x

    x = str(x).strip()

    # Decimal time value
    if ':' not in x:
        try:
            seconds = round(float(x) * 24 * 60 * 60)
            return (pd.Timestamp('2000-01-01') +
                    pd.Timedelta(seconds=seconds)).strftime('%H:%M')
        except ValueError:
            return x

    # Already in HH:MM format
    return x

df['time_orderd'] = df['time_orderd'].apply(convert_time)

df['time_order_picked'] = df['time_order_picked'].apply(convert_time)

# Clean pickup time
df['time_order_picked'] = (
    df['time_order_picked']
    .astype(str)
    .str.strip()
    .str.replace(r'^24:', '00:', regex=True)
)

df['time_orderd'] = df['time_orderd'].fillna(
    df['time_orderd'].mode()[0]
)



df['weather_conditions'] = df['weather_conditions'].fillna('Unknown')

df['road_traffic_density'] = df['road_traffic_density'].fillna('Unknown')

df['multiple_deliveries'] = df['multiple_deliveries'].fillna(0)

df['festival'] = df['festival'].fillna('No')

df['city'] = df['city'].fillna('Unknown')

print(df.duplicated().sum())
print(df['id'].duplicated().sum())

df['multiple_deliveries'] = df['multiple_deliveries'].astype(int)
df['order_date'] = pd.to_datetime(
    df['order_date'],
    format='%d-%m-%Y',
    errors='coerce'
)


df['time_order_picked'] = df['time_order_picked'].fillna(
    df['time_order_picked'].mode()[0]
)


print(df['delivery_person_age'].describe())

df.loc[df['delivery_person_age'] < 18, 'delivery_person_age'] = np.nan

df['delivery_person_age'] = df['delivery_person_age'].fillna(
    df['delivery_person_age'].median()
)
df['delivery_person_age'] = df['delivery_person_age'].astype(int)

print(df['delivery_person_ratings'].describe())
print("Ratings above 5:", (df['delivery_person_ratings'] > 5).sum())
df.loc[
    (df['delivery_person_ratings'] < 1) |
    (df['delivery_person_ratings'] > 5),
    'delivery_person_ratings'
] = np.nan
df['delivery_person_ratings'] = df['delivery_person_ratings'].fillna(
    df['delivery_person_ratings'].median()
)

print(df['time_taken_min'].describe())

print(df['delivery_person_age'].describe())
print(df['delivery_person_ratings'].describe())

df['delivery_time'] = (
    pd.to_datetime(df['time_order_picked'], format='mixed', errors='coerce')
    + pd.to_timedelta(df['time_taken_min'], unit='min')
).dt.strftime('%H:%M')

print(df.isnull().sum())
print(df.dtypes)
print(df.shape)
print(df['delivery_time'].head(5))

df.to_csv('food_delivery_cleaned.csv', index=False)




