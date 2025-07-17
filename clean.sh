# List of directories to keep (space-separated)
KEEP_DIRS="mp100 visualize resources"

echo "The following directories will be deleted:"
for dir in */; do
  # Remove trailing slash
  dir_name=${dir%/}

  # Check if dir_name is in KEEP_DIRS
  keep=false
  for keep_dir in $KEEP_DIRS; do
    if [ "$dir_name" = "$keep_dir" ]; then
      keep=true
      break
    fi
  done

  if [ "$keep" = false ]; then
    echo "  $dir"
  fi
done

printf "Do you want to delete these directories? (y/n): "
read confirm
if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
  for dir in */; do
    dir_name=${dir%/}
    keep=false
    for keep_dir in $KEEP_DIRS; do
      if [ "$dir_name" = "$keep_dir" ]; then
        keep=true
        break
      fi
    done

    if [ "$keep" = false ]; then
      rm -rf "$dir"
      echo "Deleted: $dir"
    fi
  done
else
  echo "Aborted. No directories were deleted."
fi