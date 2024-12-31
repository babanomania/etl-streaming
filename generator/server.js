const express = require('express');
const { faker } = require('@faker-js/faker');

const app = express();
const port = process.env.PORT || 3000;

const generateUser = () => {
  return {
    results: [
      {
        gender: faker.person.sex(),
        name: {
          title: faker.person.prefix(),
          first: faker.person.firstName(),
          last: faker.person.lastName(),
        },
        location: {
          street: {
            number: faker.location.streetAddress(true).split(' ')[0],
            name: faker.location.street(),
          },
          city: faker.location.city(),
          state: faker.location.state(),
          country: faker.location.country(),
          postcode: faker.location.zipCode(),
          coordinates: {
            latitude: faker.location.latitude(),
            longitude: faker.location.longitude(),
          },
          timezone: {
            offset: faker.date.recent().toString(),
            description: faker.location.timeZone(),
          },
        },
        email: faker.internet.email(),
        login: {
          uuid: faker.string.uuid(),
          username: faker.internet.username(),
          password: faker.internet.password(),
          salt: faker.string.alphanumeric(8),
          md5: faker.string.alphanumeric(32),
          sha1: faker.string.alphanumeric(40),
          sha256: faker.string.alphanumeric(64),
        },
        dob: {
          date: faker.date.past(30).toISOString(),
          age: faker.number.int({ min: 18, max: 100 }),
        },
        registered: {
          date: faker.date.past(10).toISOString(),
          age: faker.number.int({ min: 1, max: 10 }),
        },
        phone: faker.phone.number(),
        cell: faker.phone.number(),
        id: {
          name: 'SSN',
          value: faker.string.alphanumeric(11),
        },
        nat: 'US',
      },
    ],
    info: {
      seed: faker.string.uuid(),
      results: 1,
      page: 1,
      version: '1.4',
    },
  };
};

// Route to generate a random user
app.get('/api/user', (req, res) => {
  const user = generateUser();
  res.json(user);
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});
