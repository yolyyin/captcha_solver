# define parameters
USER='yint'
PI = 'rasp-008.berry.scss.tcd.ie'
JUMPER = 'macneill.scss.tcd.ie'

wget --content-disposition "https://cs7ns1.scss.tcd.ie?shortname=$USER”

# make a new folder 
mkdir ~/captchas

# Remove previous log files
rm -f successes.txt failed_downloads.txt
touch successes.txt failed_downloads.txt

# Set the number of parallel jobs
parallel_jobs=10

# Define the file processing function
process_file() {
	filename="$1"
	filename=$(echo "$filename" | tr -d '\r')

	max_retries=100
	retry_count=0
	success=false

	while [ "$retry_count" -lt "$max_retries" ]; do
		http_code=$(curl -w "%{http_code}" -o "~/captchas/$filename" -s -G "https://cs7ns1.scss.tcd.ie" \
			--data-urlencode "shortname=$USER” \
			--data-urlencode "myfilename=$filename")

		if [ "$http_code" -eq 200 ]; then
			echo "Download succeeded for $filename."
			echo "$filename" >> successes.txt
			success=true
			break
		else
			rm -f "captchas/$filename"
			((retry_count++))
			echo "Retry $retry_count/$max_retries for $filename..."
			sleep 0.1
		fi
	done

	if [ "$success" = false ]; then
		echo "$filename" >> failed_downloads.txt
	fi
}

export -f process_file

# Use xargs to process files in parallel
xargs -a $USER-challenge-filelist.csv -I{} -P "$parallel_jobs" bash -c 'process_file "$@"' _ {}

# Summarize results
success_count=$(wc -l < successes.txt 2>/dev/null || echo 0)
failed_count=$(wc -l < failed_downloads.txt 2>/dev/null || echo 0)
echo "Download completed: $success_count successful, $failed_count failed."