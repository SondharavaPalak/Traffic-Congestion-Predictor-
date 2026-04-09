# Generated migration for new analytics models

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('predictor', '0001_initial'),
    ]

    operations = [
        # Add UserProfile model
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preferred_mode', models.CharField(choices=[('Car', 'Car'), ('Metro', 'Metro'), ('Bike', 'Bike'), ('Walk', 'Walk')], default='Car', max_length=50)),
                ('car_make', models.CharField(blank=True, max_length=100, null=True)),
                ('car_mileage_kmpl', models.FloatField(default=12.0, help_text='Kilometers per liter')),
                ('fuel_cost_per_liter', models.FloatField(default=100.0)),
                ('bike_mileage_kmpl', models.FloatField(default=50.0)),
                ('primary_city', models.CharField(blank=True, max_length=100)),
                ('favorite_destinations', models.JSONField(blank=True, default=list)),
                ('commute_time_preference', models.CharField(choices=[('Fast', 'Fastest'), ('Balanced', 'Balanced Cost-Time'), ('Cheap', 'Cheapest')], default='Balanced', max_length=50)),
                ('enable_notifications', models.BooleanField(default=True)),
                ('notification_threshold', models.CharField(choices=[('Low', 'Low Traffic'), ('Medium', 'Medium Traffic'), ('High', 'High Traffic')], default='High', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='traffic_profile', to='auth.user')),
            ],
        ),
        
        # Update Prediction model with new fields and indexes
        migrations.AddField(
            model_name='prediction',
            name='probabilities',
            field=models.JSONField(blank=True, default=dict),
        ),
        
        # Add indexes to Prediction
        migrations.AddIndex(
            model_name='prediction',
            index=models.Index(fields=['user', '-created_at'], name='predictor_p_user_id_created_idx'),
        ),
        migrations.AddIndex(
            model_name='prediction',
            index=models.Index(fields=['city', 'created_at'], name='predictor_p_city_created_idx'),
        ),
        
        # Create TripHistory model
        migrations.CreateModel(
            name='TripHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100)),
                ('source', models.CharField(max_length=200)),
                ('destination', models.CharField(max_length=200)),
                ('distance_km', models.FloatField()),
                ('predicted_congestion', models.CharField(help_text='What was predicted', max_length=50)),
                ('actual_congestion', models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], help_text='What actually happened', max_length=50)),
                ('predicted_duration_mins', models.IntegerField(blank=True, null=True)),
                ('actual_duration_mins', models.IntegerField(blank=True, null=True)),
                ('mode_used', models.CharField(choices=[('Car', 'Car'), ('Metro', 'Metro'), ('Bike', 'Bike'), ('Walk', 'Walk')], max_length=50)),
                ('fuel_cost', models.FloatField(default=0)),
                ('toll_cost', models.FloatField(default=0)),
                ('total_cost', models.FloatField(default=0)),
                ('parking_cost', models.FloatField(default=0)),
                ('travel_date', models.DateTimeField()),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trip_histories', to='auth.user')),
                ('prediction', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trip_history', to='predictor.prediction')),
            ],
            options={'ordering': ['-travel_date']},
        ),
        
        # Create PredictionAccuracy model
        migrations.CreateModel(
            name='PredictionAccuracy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('total_predictions', models.IntegerField(default=0)),
                ('correct_predictions', models.IntegerField(default=0)),
                ('accuracy_percentage', models.FloatField(default=0.0)),
                ('avg_confidence', models.FloatField(default=0.0)),
                ('low_accuracy', models.IntegerField(default=0)),
                ('medium_accuracy', models.IntegerField(default=0)),
                ('high_accuracy', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accuracy_records', to='auth.user')),
            ],
            options={'ordering': ['-date']},
        ),
        
        # Create RouteOption model
        migrations.CreateModel(
            name='RouteOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100)),
                ('source', models.CharField(max_length=200)),
                ('destination', models.CharField(max_length=200)),
                ('waypoints', models.JSONField(blank=True, default=list)),
                ('route_rank', models.IntegerField(default=1)),
                ('distance_km', models.FloatField()),
                ('expected_duration_mins', models.IntegerField()),
                ('expected_congestion', models.CharField(max_length=50)),
                ('estimated_cost', models.FloatField(default=0)),
                ('mode', models.CharField(choices=[('Car', 'Car'), ('Metro', 'Metro'), ('Bike', 'Bike'), ('Walk', 'Walk')], max_length=50)),
                ('route_details', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='route_options', to='auth.user')),
            ],
            options={'ordering': ['route_rank']},
        ),
        
        # Create TripCost model
        migrations.CreateModel(
            name='TripCost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance_km', models.FloatField()),
                ('mode', models.CharField(max_length=50)),
                ('fuel_cost', models.FloatField(default=0)),
                ('toll_cost', models.FloatField(default=0)),
                ('parking_cost', models.FloatField(default=0)),
                ('metro_cost', models.FloatField(default=0)),
                ('bike_rental_cost', models.FloatField(default=0)),
                ('total_cost', models.FloatField()),
                ('cost_per_km', models.FloatField()),
                ('time_saved_mins', models.IntegerField(default=0, help_text='Time saved vs slow route')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('trip_history', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cost_details', to='predictor.triphistory')),
            ],
        ),
        
        # Create PeakHourPattern model
        migrations.CreateModel(
            name='PeakHourPattern',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100)),
                ('weekday', models.IntegerField(choices=[(0, 'Mon'), (1, 'Tue'), (2, 'Wed'), (3, 'Thu'), (4, 'Fri'), (5, 'Sat'), (6, 'Sun')])),
                ('hour', models.IntegerField()),
                ('route_type', models.CharField(max_length=50)),
                ('avg_congestion_score', models.FloatField(help_text='0-1 scale')),
                ('congestion_probability_low', models.FloatField()),
                ('congestion_probability_medium', models.FloatField()),
                ('congestion_probability_high', models.FloatField()),
                ('frequency', models.IntegerField(help_text='How many times observed')),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['city', 'weekday', 'hour']},
        ),
        
        # Create AnalyticsSnapshot model
        migrations.CreateModel(
            name='AnalyticsSnapshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('hour', models.IntegerField(blank=True, null=True)),
                ('total_predictions', models.IntegerField(default=0)),
                ('avg_congestion_score', models.FloatField(default=0.0)),
                ('avg_prediction_accuracy', models.FloatField(default=0.0)),
                ('low_congestion_count', models.IntegerField(default=0)),
                ('medium_congestion_count', models.IntegerField(default=0)),
                ('high_congestion_count', models.IntegerField(default=0)),
                ('avg_trip_duration_mins', models.FloatField(default=0.0)),
                ('avg_trip_cost', models.FloatField(default=0.0)),
                ('peak_hour', models.IntegerField(blank=True, null=True)),
                ('busiest_route', models.CharField(blank=True, max_length=400)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['-date', '-hour']},
        ),
        
        # Update SavedScenario model
        migrations.AlterField(
            model_name='savedscenario',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_scenarios', to='auth.user'),
        ),
        migrations.AddField(
            model_name='savedscenario',
            name='is_favorite',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='savedscenario',
            name='visit_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='savedscenario',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='savedscenario',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
