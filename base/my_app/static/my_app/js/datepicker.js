import {updateDateLimits} from './renderFormset.js';
const $ = window.$;

function addDatePicker() {
  const dateInputs = $('.date-input');
  const container = $('.bootstrap-iso form').length>0 ? $('.bootstrap-iso form').parent() : 'body';
  dateInputs.datepicker({
    format: 'dd/mm/yyyy',
    container,
    todayHighlight: true,
    autoclose: true,
  }).on('changeDate', updateDateLimits);
};

$(document).ready(
  addDatePicker
);

export default addDatePicker;
