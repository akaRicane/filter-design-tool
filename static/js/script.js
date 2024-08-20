document.addEventListener('DOMContentLoaded', function() {
    console.log('JavaScript is working!');

    createPageLayout();

    fetch('/getParameters')
        .then(response => response.json())
        .then(data => {
            updateParameters(data);
        });

    const generateBtn = document.getElementById('generate-schematics');
    generateBtn.addEventListener('click', function() {
        const queryParameters = {};
        const parametersWrapper = document.getElementById('parameters-wrapper');

        Array.from(parametersWrapper.children).forEach(child => {
            const label = child.children[0].textContent;
            const selectValue = child.children[1].value;
            const variable = child.children[1].id;
            queryParameters[variable] = selectValue;
        });
        
        // Convert queryParameters object to query string
        const queryString = new URLSearchParams(queryParameters).toString();
    
        fetch(`/generateSchematics?${queryString}`)
            .then(response => response.json())
            .then(data => {
                displaySVG('low-pass-svg', data.low_pass);
                displaySVG('high-pass-svg', data.high_pass);
            });
    });

    const saveBtn = document.getElementById('save-schematics');
    saveBtn.addEventListener('click', function() {
        saveBtn.textContent = 'Saving...';
        saveBtn.disabled = true;
        fetch('/saveSchematicsPng')
            .then(response => response.json())
            .then(data => {
                saveBtn.textContent = 'Save schematics';
                saveBtn.disabled = false;
            });
    });

    const sendBtn = document.getElementById('send-to-arduino');
    sendBtn.addEventListener('click', function() {
        const queryParameters = {};
        const parametersWrapper = document.getElementById('parameters-wrapper');

        Array.from(parametersWrapper.children).forEach(child => {
            const label = child.children[0].textContent;
            const selectValue = child.children[1].value;
            const variable = child.children[1].id;
            queryParameters[variable] = selectValue;
        });
        
        // Convert queryParameters object to query string
        const queryString = new URLSearchParams(queryParameters).toString();
        sendBtn.textContent = 'Sending...';
        sendBtn.disabled = true;
        fetch(`/sendArduino?${queryString}`)
        .then(response => response.json())
        .then(data => {
            sendBtn.textContent = 'Send Arduino';
            sendBtn.disabled = false;
        })
    })
    
});

function createPageLayout() {
    const root = document.getElementById('root');
    root.className = 'root';
    root.appendChild(createHeader());
    const panels = document.createElement('div');
    panels.className = 'panels';
    panels.appendChild(createLeftPanel());
    panels.appendChild(createRightPanel());
    root.appendChild(panels);
}

function createHeader() {
    const header = document.createElement('div');
    header.className = 'header';
    
    const title = document.createElement('h1');
    title.textContent = 'Filter Design Tool!';
    header.appendChild(title);

    return header;
}

function createLeftPanel() {
    const leftPanel = document.createElement('div');
    leftPanel.className = 'left-panel';

    const title = document.createElement('label');
    title.className = 'parameters-title';
    title.textContent = 'Filter parameters';
    leftPanel.appendChild(title);

    const parametersWrapper = document.createElement('div');
    parametersWrapper.id = 'parameters-wrapper';
    parametersWrapper.className = 'parameters-wrapper';
    leftPanel.appendChild(parametersWrapper);

    const generateBtn = document.createElement('button');
    generateBtn.id = 'generate-schematics';
    generateBtn.className = 'left-panel-button';
    generateBtn.textContent = 'Generate schematics';
    leftPanel.appendChild(generateBtn);

    const saveBtn = document.createElement('button');
    saveBtn.id = 'save-schematics';
    saveBtn.className = 'left-panel-button';
    saveBtn.textContent = 'Save schematics';
    leftPanel.appendChild(saveBtn);

    const sendBtn = document.createElement('button');
    sendBtn.id = 'send-to-arduino';
    sendBtn.className = 'left-panel-button';
    sendBtn.textContent = 'Send Arduino';
    leftPanel.appendChild(sendBtn);

    return leftPanel;
}

function createRightPanel() {
    const rightPanel = document.createElement('div');
    rightPanel.className = 'right-panel';

    const svgWrapper = document.createElement('div');
    svgWrapper.id = 'svg-container';
    svgWrapper.className = 'svg-container';

    const lowPassWrapper = document.createElement('div');
    lowPassWrapper.className = 'svg-wrapper';

    const lowPassTitle = document.createElement('label');
    lowPassTitle.className = 'svg-title';
    lowPassTitle.textContent = 'Low-pass filter';
    lowPassWrapper.appendChild(lowPassTitle);

    const lowPassSVG = document.createElement('svg');
    lowPassSVG.id = 'low-pass-svg';
    lowPassWrapper.appendChild(lowPassSVG);

    svgWrapper.appendChild(lowPassWrapper);

    const highPassWrapper = document.createElement('div');
    highPassWrapper.className = 'svg-wrapper';

    const highPassTitle = document.createElement('label');
    highPassTitle.className = 'svg-title';
    highPassTitle.textContent = 'High-pass filter';
    highPassWrapper.appendChild(highPassTitle);

    const highPassSVG = document.createElement('svg');
    highPassSVG.id = 'high-pass-svg';
    highPassWrapper.appendChild(highPassSVG);

    svgWrapper.appendChild(highPassWrapper);
    rightPanel.appendChild(svgWrapper);

    return rightPanel;
}

function displaySVG(target, svg) {
    const svgTarget = document.getElementById(target);
    if (svgTarget) {
        svgTarget.innerHTML = svg;
    }
}

function updateParameters(parametersDict) {
    const parametersWrapper = document.getElementById('parameters-wrapper');
    parametersWrapper.innerHTML = '';

    parametersDict.parameters.forEach(element => {
        const wrapper = document.createElement('div');
        wrapper.className = 'parameterLine'

        const label = document.createElement('label');
        label.textContent = element.label;
        wrapper.appendChild(label);

        const select = document.createElement('select');
        select.id = element.variable;
        select.value = element.default;
        select.label = element.default;
        select.default = element.default;

        parametersDict.values[element.kind].forEach(value => {
            const option = document.createElement('option');
            option.value = value;
            option.textContent = value;
            select.appendChild(option);
        });
        wrapper.appendChild(select);
        parametersWrapper.appendChild(wrapper);
    });
}