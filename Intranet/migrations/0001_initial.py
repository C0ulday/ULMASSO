# Generated by Django 4.2.5 on 2025-05-19 05:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aeronef',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=20)),
                ('tarifPilote', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('tarifElevePilote', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='BudgetBudget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(default=2025, max_length=4)),
                ('charge', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('produit', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
            ],
            options={
                'ordering': ['year'],
            },
        ),
        migrations.CreateModel(
            name='BudgetLigne',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=5)),
                ('charge', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('produit', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
            ],
            options={
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='BudgetSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=5)),
                ('charge', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('produit', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
            ],
            options={
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='ClasseULM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=1)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='CompteEpargne',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('charge', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('produit', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='Facture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default='AUV-2025-0000', max_length=13)),
                ('date', models.DateField(blank=True, null=True)),
                ('clientName', models.CharField(max_length=50)),
                ('clientVorname', models.CharField(blank=True, max_length=50, null=True)),
                ('clientZip', models.CharField(blank=True, max_length=5, null=True)),
                ('clientCity', models.CharField(blank=True, max_length=50, null=True)),
                ('clientAdress', models.CharField(blank=True, max_length=200, null=True)),
                ('clientCountry', models.CharField(default='FRANCE', max_length=50)),
            ],
            options={
                'ordering': ['-date', 'code'],
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('vorname', models.CharField(max_length=50)),
                ('password', models.CharField(default='0000', max_length=20)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, max_length=14, null=True)),
                ('email', models.EmailField(blank=True, max_length=50, null=True)),
                ('zip', models.CharField(blank=True, max_length=5, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('adress', models.CharField(blank=True, max_length=200, null=True)),
                ('licenceFFPLUM', models.CharField(blank=True, max_length=6, null=True)),
                ('datePiloteC2', models.DateField(blank=True, null=True)),
                ('datePiloteC3', models.DateField(blank=True, null=True)),
                ('datePiloteC4', models.DateField(blank=True, null=True)),
                ('dateEmportC2', models.DateField(blank=True, null=True)),
                ('dateEmportC3', models.DateField(blank=True, null=True)),
                ('dateEmportC4', models.DateField(blank=True, null=True)),
                ('dateBaptemeC2', models.DateField(blank=True, null=True)),
                ('dateBaptemeC3', models.DateField(blank=True, null=True)),
                ('dateBaptemeC4', models.DateField(blank=True, null=True)),
                ('reportComptePilote2024', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('produitComptePilote', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('chargeComptePilote', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
            ],
            options={
                'ordering': ['name', 'vorname'],
            },
        ),
        migrations.CreateModel(
            name='OuiNon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Sex',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.CharField(default='M', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Statut',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Vol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('textVVent', models.CharField(blank=True, default='RAS', max_length=1000)),
                ('textAltitude', models.CharField(blank=True, default='RAS', max_length=1000)),
                ('textStress', models.CharField(blank=True, default='RAS', max_length=1000)),
                ('textDecollage', models.CharField(blank=True, default='RAS', max_length=1000)),
                ('textVol', models.CharField(blank=True, default='RAS', max_length=1000)),
                ('textNav', models.CharField(blank=True, default='RAS', max_length=1000)),
                ('textRadio', models.CharField(blank=True, default='RAS', max_length=1000)),
                ('textAtterrissage', models.CharField(blank=True, default='RAS', max_length=1000)),
                ('textTdp', models.CharField(blank=True, default='RAS', max_length=1000)),
                ('textBaseULM', models.CharField(blank=True, default='RAS', max_length=1000)),
                ('textCommentaire', models.CharField(blank=True, default='RAS', max_length=1000)),
                ('instructeur', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('horoInit', models.DecimalField(decimal_places=2, default=0.0, max_digits=7)),
                ('horoFin', models.DecimalField(decimal_places=2, default=0.0, max_digits=7)),
                ('prixVol', models.DecimalField(decimal_places=2, default=0.0, max_digits=7)),
                ('tarifInstruction', models.DecimalField(decimal_places=2, default=0.0, max_digits=7)),
                ('remise', models.DecimalField(decimal_places=2, default=0.0, max_digits=7)),
                ('aeronef', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Intranet.aeronef')),
                ('bapteme', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='baptemeOuiNon', to='Intranet.ouinon')),
                ('indemInstructeur', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='idemInstructeurOuiNon', to='Intranet.ouinon')),
                ('maintenance', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='maintenanceOuiNon', to='Intranet.ouinon')),
                ('pilote', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Intranet.member')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='OperationFacture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default='PXXXX-XXXX', max_length=10)),
                ('objet', models.CharField(max_length=150)),
                ('prixHT', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('nb', models.IntegerField(default=1)),
                ('facture', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Intranet.facture')),
                ('ligne', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='Intranet.budgetligne')),
            ],
        ),
        migrations.AddField(
            model_name='member',
            name='brevetInstructeur',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='brevetInstructeurOuiNon', to='Intranet.ouinon'),
        ),
        migrations.AddField(
            model_name='member',
            name='genre',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Intranet.sex'),
        ),
        migrations.AddField(
            model_name='member',
            name='licenceAUV',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='licenceAUVOuiNon', to='Intranet.ouinon'),
        ),
        migrations.AddField(
            model_name='member',
            name='statut',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, to='Intranet.statut'),
        ),
        migrations.AddField(
            model_name='facture',
            name='acquite',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='acquiteOuiNon', to='Intranet.ouinon'),
        ),
        migrations.CreateModel(
            name='CompteEpargneOperation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(default='CE-0000', max_length=9)),
                ('charge', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('produit', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('compteEpargne', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Intranet.compteepargne')),
            ],
            options={
                'ordering': ['-date', 'code'],
            },
        ),
        migrations.CreateModel(
            name='BudgetProjet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=5)),
                ('charge', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('produit', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('section', models.ForeignKey(default=0, null=True, on_delete=django.db.models.deletion.CASCADE, to='Intranet.budgetsection')),
            ],
            options={
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='BudgetOperation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(default='PXXXX-0000', max_length=10)),
                ('charge', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('produit', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('aeronef', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Intranet.aeronef')),
                ('beneficiaire', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Intranet.member')),
                ('budget', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='Intranet.budgetbudget')),
                ('ligne', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Intranet.budgetligne')),
            ],
            options={
                'ordering': ['-date', 'code'],
            },
        ),
        migrations.AddField(
            model_name='budgetligne',
            name='projet',
            field=models.ForeignKey(default=0, null=True, on_delete=django.db.models.deletion.CASCADE, to='Intranet.budgetprojet'),
        ),
        migrations.AddField(
            model_name='aeronef',
            name='classeULM',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='Intranet.classeulm'),
        ),
    ]
