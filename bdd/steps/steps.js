import { Given, When, Then } from '@cucumber/cucumber';
import fetch from 'node-fetch';
import { expect } from 'chai';

let response;

Given('the API is running', async function () {
    response = null;
});

When('I send the prompt {string}', async function (prompt) {
    const res = await fetch('http://localhost:8000/evaluate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt })
    });
    response = await res.json();
});

Then('the response should contain {string}', function (expected) {
    expect(response).to.have.property('response');
    expect(response.response).to.include(expected);
});

