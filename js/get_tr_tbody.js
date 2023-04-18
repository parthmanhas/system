// get the tbody element
const tbody = document.querySelector('.section_medium_spacing > div:nth-child(1) > div:nth-child(2) > table:nth-child(1) > tbody:nth-child(2)');

// create an array to store the third td values
const dates = [];

// loop over the tr elements in the tbody
for (let i = 0; i < tbody.children.length; i++) {
    const tr = tbody.children[i];

    // get the third td element in the tr
    const thirdTd = tr.children[2];

    const dateStr = thirdTd.textContent.trim();

    const dateObj = new Date(dateStr);

    // get the year, month (0-indexed), and day from the date object
    const year = dateObj.getFullYear();
    const month = dateObj.getMonth() + 1; // add 1 because months are 0-indexed
    const day = dateObj.getDate();

    // convert the year, month, and day to a string in the 'YYYY-MM-DD' format
    const formattedDate = `${year}-${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`;


    // get the text content of the third td element and push it to the array
    dates.push(formattedDate);
}

// output the third td values array
console.log(dates);

[
    "NaN-NaN-NaN",
    "2017-01-26",
    "2017-02-24",
    "2017-03-13",
    "2017-04-04",
    "2017-04-14",
    "2017-04-14",
    "2017-05-01",
    "2017-06-26",
    "2017-08-15",
    "2017-08-25",
    "2017-10-02",
    "2017-10-19",
    "2017-10-20",
    "2017-12-25"
  ]

  [
    "NaN-NaN-NaN",
    "2018-01-26",
    "2018-02-13",
    "2018-03-02",
    "2018-03-29",
    "2018-03-30",
    "2018-05-01",
    "2018-08-15",
    "2018-05-22",
    "2018-09-13",
    "2018-09-20",
    "2018-10-02",
    "2018-10-18",
    "2018-11-07",
    "2018-11-08",
    "2018-11-23",
    "2018-12-25"
  ]

  [
    "NaN-NaN-NaN",
    "2019-03-04",
    "2019-03-21",
    "2019-04-17",
    "2019-04-19",
    "2019-05-01",
    "2019-06-05",
    "2019-08-12",
    "2019-08-15",
    "2019-09-02",
    "2019-09-10",
    "2019-10-02",
    "2019-10-08",
    "2019-10-28",
    "2019-11-12",
    "2019-12-25"
  ]

  [
    "NaN-NaN-NaN",
    "2020-02-21",
    "2020-03-10",
    "2020-04-02",
    "2020-04-06",
    "2020-04-10",
    "2020-04-14",
    "2020-05-01",
    "2020-05-25",
    "2020-10-02",
    "2020-11-16",
    "2020-11-30",
    "2020-12-25"
  ]

  [
    "NaN-NaN-NaN",
    "2021-01-26",
    "2021-03-11",
    "2021-03-29",
    "2021-04-02",
    "2021-04-14",
    "2021-04-21",
    "2021-05-13",
    "2021-07-21",
    "2021-08-19",
    "2021-09-10",
    "2021-10-15",
    "2021-11-04",
    "2021-11-05",
    "2021-11-19"
  ]

  [
    "2022-01-26",
    "2022-03-01",
    "2022-03-18",
    "2022-04-14",
    "2022-04-15",
    "2022-05-03",
    "2022-08-09",
    "2022-08-15",
    "2022-08-31",
    "2022-10-05",
    "2022-10-24",
    "2022-10-26",
    "2022-11-08"
  ]

  [
    "2023-01-26",
    "2023-03-07",
    "2023-03-30",
    "2023-04-04",
    "2023-04-07",
    "2023-04-14",
    "2023-05-01",
    "2023-06-28",
    "2023-08-15",
    "2023-09-19",
    "2023-10-02",
    "2023-10-24",
    "2023-11-14",
    "2023-11-27",
    "2023-12-25"
  ]