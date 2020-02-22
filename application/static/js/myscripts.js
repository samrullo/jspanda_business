$(document).ready(function() {
  $('#myTable').DataTable({
    'order': [
      [$("")]
    ]
  });
  $('#jspanda_orders_table').DataTable({
    'order': [
      [0, 'desc']
    ]
  });


  //first get order_col_no which specifies what columns should be used for ordering
  var order_col_no = Number($(".orderByDateTable thead").attr("order_col_no"))
  if (order_col_no == "" || order_col_no == null) {
    order_col_no = 0;
  }
  $('.orderByDateTable').DataTable({
    'order': [
      [order_col_no, 'desc']
    ]
  });
  $('.dataTables_length').addClass('bs-select');
});



function tableSearch() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}
