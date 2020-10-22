/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 1);
/******/ })
/************************************************************************/
/******/ ({

/***/ "./src/js/scope.js":
/*!*************************!*\
  !*** ./src/js/scope.js ***!
  \*************************/
/*! no static exports found */
/***/ (function(module, exports) {

///////////////////////////////////  Scope page     ///////////////////////////////
var scope_import_btn = document.getElementsByClassName("scope__add-btn")[0];
var toggle_all_btn = document.getElementById("get-all");
var delete_selected_btn = document.getElementsByClassName("scope__delete")[0];
scope_import_btn.addEventListener("click", function (event) {
  event.preventDefault();
  var scope_hosts = document.querySelector("input[name=scope_hosts]");
  var reader = new FileReader();

  if (scope_hosts.files.length) {
    reader.readAsText(scope_hosts.files[0]);

    reader.onload = function () {
      fetch(SERVER_PROTO + SERVER_HOST + "/api/project/importScope", {
        method: "post",
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          project_id: project_id,
          scope_hosts: reader.result
        })
      }).then(function (response) {
        return response.json();
      }).then(function (data) {
        if (data.status === 1) {
          var scope_modal_elem = document.getElementById('scopeModal');
          var scope_modal = coreui.Modal.getInstance(scope_modal_elem);
          scope_modal.hide();
          var success_modal = new coreui.Modal(document.getElementById('successModal'));

          if (data.invalid_hosts.length > 0) {
            success_modal._element.childNodes[1].children[0].childNodes[3].innerText = "Invalid hosts that did not added:";

            for (var i = 0; i < data.invalid_hosts.length; i++) {
              var item_li = document.createElement('li');
              item_li.className = "invalid_host";
              item_li.innerText = "".concat(data.invalid_hosts[i]);

              success_modal._element.childNodes[1].children[0].childNodes[3].append(item_li);
            }
          }

          success_modal.show();
          document.getElementById('successModal').addEventListener('hide.coreui.modal', function (e) {
            window.location = "";
          }, false);
        } else {
          alert(data.error);
        }
      })["catch"](function (error) {
        return alert(error);
      });
    };
  }
});
toggle_all_btn.addEventListener("click", function (e) {
  var checkboxes = document.getElementsByClassName("host-chbox");

  if (!e.target.checked) {
    for (var i = 0; i < checkboxes.length; i++) {
      checkboxes[i].checked = false;
    }
  } else {
    for (var _i = 0; _i < checkboxes.length; _i++) {
      checkboxes[_i].checked = true;
    }
  }
});
delete_selected_btn.addEventListener("click", function () {
  var hosts_for_delete = [];
  var chboxes = document.getElementsByClassName("host-chbox");
  [].forEach.call(chboxes, function (chbox) {
    if (chbox.checked) {
      var tr = chbox.closest("tr");
      var ip = tr.querySelector(".scope__ip");
      var domain = tr.querySelector(".scope__domain");

      if (ip.innerHTML !== "-") {
        hosts_for_delete.push(ip.innerHTML);
      }

      if (domain.innerHTML !== "-") {
        hosts_for_delete.push(domain.innerHTML);
      }
    }
  });

  if (hosts_for_delete.length) {
    var is_delete = confirm("Are you sure you want to delete selected hosts ?");

    if (is_delete) {
      fetch(SERVER_PROTO + SERVER_HOST + "/api/project/deleteScope", {
        method: "post",
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          project_id: project_id,
          delete_hosts: hosts_for_delete
        })
      }).then(function (response) {
        return response.json();
      }).then(function (data) {
        if (data.status === 1) {
          var delete_modal = new coreui.Modal(document.getElementById('deleteModal'));
          delete_modal.show();
          document.getElementById('deleteModal').addEventListener('hide.coreui.modal', function (e) {
            window.location = "";
          }, false);
        } else if (data.status === 0) {
          alert(data.error);
        }
      })["catch"](function (error) {
        alert(error);
      });
    }
  }
});

/***/ }),

/***/ 1:
/*!*******************************!*\
  !*** multi ./src/js/scope.js ***!
  \*******************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(/*! ./src/js/scope.js */"./src/js/scope.js");


/***/ })

/******/ });
//# sourceMappingURL=scope.js.map