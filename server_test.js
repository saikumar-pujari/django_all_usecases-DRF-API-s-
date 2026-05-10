// this will test the server with 50 requests per second for 3 seconds, with a maximum of 500 virtual users. You can adjust the rate, duration, and number of virtual users as needed.

//you adjust it according to your needs, for example, you can increase the rate to 100 requests per second, or increase the duration to 10 seconds, or increase the maximum number of virtual users to 1000. Just make sure to adjust the preAllocatedVUs accordingly to avoid running out of virtual users during the test.


import http from 'k6/http';

export const options = {
    scenarios: {
        constant_load: {
            executor: 'constant-arrival-rate',
            rate: 50,
            timeUnit: '1s',
            duration: '3s',
            preAllocatedVUs: 100,
            maxVUs: 500,
        },
    },
};

export default function () {
    http.get('http://127.0.0.1:8000/n1/');
}

// k6 run server_test.js