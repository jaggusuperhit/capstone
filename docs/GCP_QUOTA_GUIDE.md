# GCP Quota Management Guide

This guide provides information on how to manage GCP quotas and resolve quota-related issues when creating a GKE cluster.

## Understanding the Quota Issue

When creating a GKE cluster, you encountered the following error:

```
Insufficient regional quota to satisfy request: resource "SSD_TOTAL_GB": request requires '600.0' and is short '100.0'. project has a quota of '500.0' with '500.0' available.
```

This means that your GCP project doesn't have enough SSD quota in the us-central1 region to create the requested cluster.

## Options to Resolve Quota Issues

### Option 1: Request a Quota Increase

You can request a quota increase from Google Cloud:

1. Go to the [IAM & Admin > Quotas & System Limits](https://console.cloud.google.com/iam-admin/quotas) page in the Google Cloud Console
2. Filter for "SSD_TOTAL_GB" and select the quota for the us-central1 region
3. Click "EDIT QUOTAS" at the top of the page
4. Enter the new quota limit (at least 600 GB for your current configuration)
5. Fill in your contact information and submit the request

Note that quota increase requests may take 24-48 hours to be approved.

### Option 2: Use Standard Disks Instead of SSDs

You can use standard persistent disks instead of SSDs, which have different quota limits:

```powershell
.\scripts\create_gke_cluster.ps1
```

We've updated this script to use standard disks instead of SSDs.

### Option 3: Use a Different Region

You can try creating the cluster in a different region where you might have more quota available:

```powershell
.\scripts\create_gke_cluster_alt_region.ps1
```

This script will create the cluster in the us-west1 region.

### Option 4: Use a Zonal Cluster Instead of a Regional Cluster

Regional clusters require more resources than zonal clusters. You can create a zonal cluster instead:

```powershell
.\scripts\create_gke_cluster_zonal.ps1
```

This script will create a zonal cluster in the us-central1-a zone.

### Option 5: Reduce Cluster Size

You can reduce the size of the cluster by using smaller machine types and fewer nodes:

- We've already updated the scripts to use e2-small machine type instead of e2-standard-2
- We've reduced the number of nodes from 2 to 1

## Checking Your Current Quotas

To check your current quotas:

```bash
gcloud compute regions describe us-central1 --format="yaml(quotas)"
```

This will show you all the quotas for the us-central1 region.

## After Creating the Cluster

After successfully creating the cluster using one of the options above, you can deploy your application using the corresponding deployment script:

- For the standard regional cluster: `.\scripts\deploy_to_gke.ps1`
- For the alternative region cluster: `.\scripts\deploy_to_gke.ps1` (automatically updated)
- For the zonal cluster: `.\scripts\deploy_to_gke_zonal.ps1`
