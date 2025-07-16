KEEP_DIR="mp100"

echo "The following directories will be deleted:"
for dir in */; do
  if [ "$dir" != "$KEEP_DIR/" ]; then
    echo "  $dir"
  fi
done

printf "Do you want to delete these directories? (y/n): "
read confirm
if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
  for dir in */; do
    if [ "$dir" != "$KEEP_DIR/" ]; then
      rm -rf "$dir"
      echo "Deleted: $dir"
    fi
  done
else
  echo "Aborted. No directories were deleted."
fi