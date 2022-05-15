window.onload = function() {
    let addgradeFieldBtn = document.getElementById('add-course-field');
    addgradeFieldBtn.addEventListener('click', function(e){
        e.preventDefault();
        let allgradesFieldWrapper = document.getElementById('grades');
        let allgradesField = allgradesFieldWrapper.getElementsByTagName('input');
        if(allgradesField.length > 9) {
            alert('You can have only ten grades');
            return;
        }
        let gradeInputIds = []
        for(let i = 0; i < allgradesField.length; i++) {
            gradeInputIds.push(parseInt(allgradesField[i].name.split('-')[1]));
        }
        let newFieldName = `grades-${Math.max(...gradeInputIds) + 1}`;
        allgradesFieldWrapper.insertAdjacentHTML('beforeend',`
        <li><label for="${newFieldName}"></label> <input id="${newFieldName}" name="${newFieldName}" type="number" value=""></li> 
        `);

        let allcoursesFieldWrapper = document.getElementById('courses');
        let allcoursesField = allcoursesFieldWrapper.getElementsByTagName('input');
        if(allcoursesField.length > 9) {
            alert('You can have only ten grades');
            return;
        }
        let courseInputIds = []
        for(let i = 0; i < allcoursesField.length; i++) {
            courseInputIds.push(parseInt(allcoursesField[i].name.split('-')[1]));
        }
        let newFieldCourse = `courses-${Math.max(...gradeInputIds) + 1}`;
        allcoursesFieldWrapper.insertAdjacentHTML('beforeend',`
        <li><label for="${newFieldCourse}"></label> <input id="${newFieldCourse}" name="${newFieldCourse}" type="text" value=""></li>`);
    });

    let removegradeFieldBtn = document.getElementById('remove-course-field');
    removegradeFieldBtn.addEventListener('click', function(e){
        e.preventDefault();
        var select = document.getElementById('courses');
        select.removeChild(select.lastElementChild);
        var select = document.getElementById('grades');
        select.removeChild(select.lastElementChild);
    });}