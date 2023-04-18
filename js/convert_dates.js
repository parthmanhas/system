// input array of date strings
const dateStrArray = ['January 26, 2023', 'March 07, 2023', 'March 30, 2023', 'April 04, 2023', 'April 07, 2023', 'April 14, 2023', 'May 01, 2023', 'June 28, 2023', 'August 15, 2023', 'September 19, 2023', 'October 02, 2023', 'October 24, 2023', 'November 14, 2023', 'November 27, 2023', 'December 25, 2023'];

// create an empty array to store the formatted dates
const formattedDateArray = [];

// loop over the input date string array and convert each string to the 'YYYY-MM-DD' format
for (let i = 0; i < dateStrArray.length; i++) {
  const dateStr = dateStrArray[i];
  const dateObj = new Date(dateStr);
  const year = dateObj.getFullYear();
  const month = dateObj.getMonth() + 1;
  const day = dateObj.getDate();
  const formattedDate = `${year}-${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`;
  formattedDateArray.push(formattedDate);
}

// output the formatted date array
console.log(formattedDateArray);