const $ = window.$;
const getDateLimits = window.getDateLimits;

function addDatePicker() {
  const dateInputs = $('.date-input');
  const container = $('.bootstrap-iso form').length>0 ? $('.bootstrap-iso form').parent() : 'body';
  dateInputs.datepicker({
    format: 'dd/mm/yyyy',
    container,
    todayHighlight: true,
    autoclose: true,
  }).on('changeDate', getDateLimits);
};

$(document).ready(
  addDatePicker
);
