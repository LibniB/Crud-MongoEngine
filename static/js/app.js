//ventana emergente de confirmacion para eliminar producto.

document.addEventListener('DOMContentLoaded', function () {
  const deleteIcons = document.querySelectorAll('.delete-icon');
  deleteIcons.forEach(icon => {
      icon.addEventListener('click', function (event) {
          event.preventDefault(); // Evitar el comportamiento predeterminado del enlace

          const productId = this.getAttribute('data-id');

          // ventana emergente
          Swal.fire({
              title: '¿Estás seguro de querer eliminar este producto?',
              icon: 'warning',
              showCancelButton: true,
              confirmButtonText: 'Sí',
              cancelButtonText: 'Cancelar'
          }).then((result) => {
              if (result.isConfirmed) {
                  window.location.href = '/eliminarProducto/' + productId;
              }
          });
      });
  });
});

//ventana emergente de confirmacion para editar producto.

document.addEventListener('DOMContentLoaded', function () {
  const editIcons = document.querySelectorAll('.edit-icon');
  editIcons.forEach(icon => {
      icon.addEventListener('click', function (event) {
          event.preventDefault(); // Evitar el comportamiento predeterminado del enlace

          const productId = this.getAttribute('data-id');

          Swal.fire({
              title: '¿Estás seguro de querer editar este producto?',
              icon: 'warning',
              showCancelButton: true,
              confirmButtonText: 'Sí',
              cancelButtonText: 'Cancelar'
          }).then((result) => {
              // Si se hace clic en "Sí", redirigir para editar el producto
              if (result.isConfirmed) {
                  window.location.href = '/editarProducto/' + productId;
              }
          });
      });
  });
});


function cancelarRegistro() {
  window.location.href = '/iniciarSesion';
}

// funcion para visualizar la foto
function visualizarFoto(event) {
  imagenProducto = document.getElementById('imagenProducto');
  
  if (event.target.files && event.target.files[0]) {
      var reader = new FileReader();

      reader.onload = function (e) {
          imagenProducto.src = e.target.result;
      }

      // Leer el archivo como una URL de datos
      reader.readAsDataURL(event.target.files[0]);
  } else {
      imagenProducto.src = '';
  }
}