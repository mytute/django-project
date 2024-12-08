#!/bin/bash

# Array of branch names
branches=(
  "1 - Getting Started"
  "2 - Applications and Routes"
  "3 - Templates"
  "4 - Admin Page"
  "5 - Database and Migrations"
  "6 - User Registration"
  "7 - Login and Logout System"
  "8 - User Profile and Picture"
  "9 - Update User Profile"
  "10 - Create, Update, and Delete Posts"
  "11 - Pagination"
  "12 - Email and Password Reset"
  "13 - Deploying Your Application (Option #1) - Deploy to a Linux Server"
  "14 - How to Use a Custom Domain Name for Our Application"
  "15 - How to enable HTTPS with a free SSL/TLS Certificate using Let's Encrypt"
  "16 - Full-Featured Web App Part 13 - Using AWS S3 for File Uploads"
  "17 - Deploying Your Application (Option #2) - Deploy using Heroku"
)

# Function to format the branch name
format_branch_name() {
  echo "$1" | sed -E 's/[^a-zA-Z0-9]+/_/g' | sed -E 's/^_+|_+$//g' | tr '[:upper:]' '[:lower:]'
}

# Create branches
for branch in "${branches[@]}"; do
  # Extract the prefix number and description
  prefix=$(echo "$branch" | cut -d' ' -f1)
  description=$(echo "$branch" | cut -d' ' -f3-)

  # Format the branch name
  formatted_name=$(format_branch_name "$description")

  # Combine to create the final branch name
  branch_name="project/$(printf '%03d' "$prefix")_$formatted_name"

  # Create the branch
  echo "Creating branch: $branch_name"
  git branch "$branch_name"
done

# Print all created branches
echo "All branches have been created!"
git branch
