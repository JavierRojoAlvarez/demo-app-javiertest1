import addDatePicker from './datepicker.js';
const moment = window.moment;
const endpoint = window.endpoint;
const amountInput = document.getElementById('id_amount');
const addBtn = document.getElementById('btn-add');
const formsetDiv = document.getElementById('formset');
const tokenVal = document.getElementsByName('csrfmiddlewaretoken')[0].value;
const pseudoSelect = document.getElementById('id_transaction_type');

function updateDateLimits() {
  const startDate = document.getElementById('start-date');
  const endDate = document.getElementById('end-date');
  const dateInputs = formsetDiv.querySelectorAll('.date-input');
  if (startDate && endDate && dateInputs) {
    const dates =[];
    for (const date of dateInputs.values()) {
      if (!dates.includes(date.value)) {
        dates.push(date.value);
      };
    };
    const momentDates =[];
    for (const date of dates) {
      const momentDate = moment(date, 'DD/MM/YYYY');
      if (momentDate.isValid()) {
        momentDates.push(momentDate);
      };
    };
    const minDate = moment.min(momentDates);
    const maxDate = moment.max(momentDates);
    if (momentDates.length === 0) {
      startDate.innerHTML='- - -';
      endDate.innerHTML='- - -';
    } else {
      startDate.innerHTML = minDate.format('Do MMMM YYYY');
      endDate.innerHTML = maxDate.format('Do MMMM YYYY');
    };
  };
};

function dateListener() {
  formsetDiv.querySelectorAll('.date-input').forEach(function(el) {
    el.addEventListener('input', function() {
      updateDateLimits();
    });
  });
};

function makeDecimal() {
  amountInput.value = parseFloat(parseFloat(amountInput.value).toFixed(2));
};

function getFormsetValues() {
  const fieldElements = formsetDiv.querySelectorAll('#formset input, select');
  const myObj = {};
  for (const element of fieldElements.values()) {
    myObj[element.name] = element.value;
  };
  console.log('Current formset values...');
  console.log(myObj);
  return JSON.stringify(myObj);
};

function changeTransactionAmounts() {
  const elems = formsetDiv.querySelectorAll('.amount');
  let index = 0;
  const length = elems.length;
  console.log(amountInput.value);
  for (; index < length; index++) {
    elems[index].value = amountInput.value;
  };
  console.log('Changed amounts in formset');
};

function changeEntryAmounts() {
  const formset2Div = document.getElementById('formset2');
  const amountInputs = formset2Div.querySelectorAll('.amount');
  const total = getTransactionAmounts();
  for (const amountInput of amountInputs.values()) {
    amountInput.value = total;
  };
  console.log('Changed entry values');
};

if (document.body.contains(document.getElementById('formset2'))) {
  changeEntryAmounts();
};

function getTransactionAmounts() {
  const transactionAmountInputs = formsetDiv.querySelectorAll('.amount');
  let total = 0.00;
  for (const transactionAmountInput of transactionAmountInputs.values()) {
    console.log(transactionAmountInput.value);
    total += parseFloat(transactionAmountInput.value);
  }
  console.log('Transaction amount total: ' + total);
  return total.toFixed(2);
};

function transactionAmountListener() {
  const transactionAmountInputs = formsetDiv.querySelectorAll('.amount');
  for (const el of transactionAmountInputs.values()) {
    el.addEventListener('input', changeEntryAmounts);
  };
};

function removeRowListener() {
  document.querySelectorAll('.btn-remove-row').forEach(function(el) {
    el.addEventListener('click', function() {
      getFormset(null, this.id, null, null);
      console.log('Removed row at index: ' + this.id);
    });
  });
};

function getFormset(addEntry, removeEntryIndex, amountDecimal, transactionTypeId) {
  console.log(
    '%c getFormset() Initiated',
    'background: cornflowerblue; color: white; padding: 2px; border-radius:2px'
  );
  fetch(endpoint, {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'X-CSRFToken': tokenVal
    },
    body: JSON.stringify({
      amount: amountDecimal,
      parent_type: transactionTypeId,
      add_entry: addEntry,
      remove_entry: removeEntryIndex,
      current_data: JSON.parse(getFormsetValues())
    }),
    credentials: 'same-origin'
  }).then(response => response.text())
    .then(function(htmlData) {
      document.getElementById('formset').innerHTML = htmlData;
      transactionAmountListener();
      changeEntryAmounts();
      removeRowListener();
      addDatePicker();
      dateListener();
      updateDateLimits();
      console.log(
        '%c getFormset() Successful',
        'background: mediumseagreen; color: white; padding: 2px; border-radius:2px'
      );
    })
    .catch(error => console.log(error));
};

amountInput.addEventListener('input', function() {
  makeDecimal();
  changeTransactionAmounts();
});

addBtn.addEventListener('click', function() {
  getFormset(true, null, null, null);
});

if (pseudoSelect) {
  pseudoSelect.addEventListener('change', function() {
    getFormset(null, null, amountInput.value, pseudoSelect.value);
  });
};

removeRowListener();
transactionAmountListener();
dateListener();
updateDateLimits();

export {updateDateLimits};
