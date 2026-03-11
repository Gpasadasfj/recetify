document.addEventListener("DOMContentLoaded", function () {
    const addButton = document.getElementById("add-step");
    const container = document.getElementById("steps-container");
    const totalForms = document.querySelector('input[name="steps-TOTAL_FORMS"]');

    addButton.addEventListener("click", () => {
        const stepCount = parseInt(totalForms.value);
    
        const lastStep = container.querySelector(".step-item:last-child");
        const newStep = lastStep.cloneNode(true);
    
        const textarea = newStep.querySelector("textarea");
        textarea.value = "";
        textarea.name = `steps-${stepCount}-description`;
        textarea.id = `id_steps-${stepCount}-description`;
    
        newStep.querySelector(".step-label").innerText = stepCount + 1;
    
        container.appendChild(newStep);
        totalForms.value = stepCount + 1;
    });
})

