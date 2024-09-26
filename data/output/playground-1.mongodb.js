// Select the database to use.
use('cookbookapp');

// Run a find command to view items sold on April 4th, 2014 and project the title field.
const salesOnApril4th = db.getCollection('data').find(
  {'id': 642583},
  {'title': 1, '_id': 0} // Project the title field and exclude the _id field
).toArray;
