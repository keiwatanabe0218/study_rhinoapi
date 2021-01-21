let args = {
    algo : null, 
    pointer : null,
    values : []
};

let definition = null;

// get slider values
let X = document.getElementById('X').value;
let Y = document.getElementById('Y').value;
let Z = document.getElementById('Z').value;
let M_st = document.getElementById('M_st').value;
let D_st = document.getElementById('D_st').value;
let H_st = document.getElementById('H_st').value;
let M_ed = document.getElementById('M_ed').value;
let D_ed = document.getElementById('D_ed').value;
let H_ed = document.getElementById('H_ed').value;

let param1 = new RhinoCompute.Grasshopper.DataTree('RH_IN:201:Y');
param1.append([0], [Y]);

let param2 = new RhinoCompute.Grasshopper.DataTree('RH_IN:201:X');
param2.append([0], [X]);

let param3 = new RhinoCompute.Grasshopper.DataTree('RH_IN:201:Z');
param3.append([0], [Z]);

let param4 = new RhinoCompute.Grasshopper.DataTree('RH_IN:201:M_st');
param4.append([0], [M_st]);
let param5 = new RhinoCompute.Grasshopper.DataTree('RH_IN:201:D_st');
param5.append([0], [D_st]);
let param6 = new RhinoCompute.Grasshopper.DataTree('RH_IN:201:H_st');
param6.append([0], [H_st]);

let param7 = new RhinoCompute.Grasshopper.DataTree('RH_IN:201:M_ed');
param7.append([0], [M_ed]);
let param8 = new RhinoCompute.Grasshopper.DataTree('RH_IN:201:D_ed');
param8.append([0], [D_ed]);
let param9 = new RhinoCompute.Grasshopper.DataTree('RH_IN:201:H_ed');
param9.append([0], [H_ed]);

rhino3dm().then(async m => {
    console.log('Loaded rhino3dm.');
    rhino = m; // global

    RhinoCompute.url = "http://localhost:8081/" // Rhino.Compute server url
    // RhinoCompute.apiKey = "" // your Rhino.Compute server api key

    // load a grasshopper file!
    let url = '/static/resources/grasshopper/ladybug_test01.gh';
    let res = await fetch(url);
    let buffer = await res.arrayBuffer();
    let arr = new Uint8Array(buffer);
    definition = arr;
    THREE.Object3D.DefaultUp = new THREE.Vector3(0,0,1)
    init();
    compute();
});

function compute(){

    // clear values
    let trees = [];

    trees.push(param1);
    trees.push(param2);
    trees.push(param3);
    trees.push(param4);
    trees.push(param5);
    trees.push(param6);
    trees.push(param7);
    trees.push(param8);
    trees.push(param9);


    RhinoCompute.Grasshopper.evaluateDefinition(definition, trees).then(result => {
        // RhinoCompute.computeFetch("grasshopper", args).then(result => {
        // console.log(result);

        // hide spinner
        document.getElementById('loader').style.display = 'none';
        console.log(result.values)
        let data = JSON.parse(result.values[0].InnerTree['{ 0; }'][0].data);

        let context = JSON.parse(result.values[1].InnerTree['{ 0; }'][0].data);

        let mesh = rhino.CommonObject.decode(data);
        let context_mesh = rhino.CommonObject.decode(context);

        // let material = new THREE.MeshNormalMaterial();
        var material = new THREE.MeshBasicMaterial({vertexColors: THREE.VertexColors});
        let threeMesh = meshToThreejs(mesh, material);

        let context_material = new THREE.MeshNormalMaterial();
        let context_threeMesh = meshToThreejs(context_mesh, context_material);
        // clear meshes from scene

        scene.traverse(child => {
            if(child.type === 'Mesh'){
                scene.remove(child);
            }
        });

        scene.add(threeMesh);
        scene.add(context_threeMesh)
    });
}

function onSliderChange(){

    // show spinner
    document.getElementById('loader').style.display = 'block';

    // get slider values
    X = document.getElementById('X').value;
    Y = document.getElementById('Y').value;
    Z = document.getElementById('Z').value;
    M_st = document.getElementById('M_st').value;
    D_st = document.getElementById('D_st').value;
    H_st = document.getElementById('H_st').value;
    M_ed = document.getElementById('M_ed').value;
    D_ed = document.getElementById('D_ed').value;
    H_ed = document.getElementById('H_ed').value;


    param1 = new RhinoCompute.Grasshopper.DataTree('RH_IN:201:Y');
    param1.append([0], [Y]);

    param2 = new RhinoCompute.Grasshopper.DataTree('RH_IN:201:X');
    param2.append([0], [X]);

    param3 = new RhinoCompute.Grasshopper.DataTree('RH_IN:201:Z');
    param3.append([0], [Z]);

    param4 = new RhinoCompute.Grasshopper.DataTree('RH_IN:201:M_st');
    param4.append([0], [M_st]);
    param5 = new RhinoCompute.Grasshopper.DataTree('RH_IN:201:D_st');
    param5.append([0], [D_st]);
    param6 = new RhinoCompute.Grasshopper.DataTree('RH_IN:201:H_st');
    param6.append([0], [H_st]);

    param7 = new RhinoCompute.Grasshopper.DataTree('RH_IN:201:M_ed');
    param7.append([0], [M_ed]);
    param8 = new RhinoCompute.Grasshopper.DataTree('RH_IN:201:D_ed');
    param8.append([0], [D_ed]);
    param9 = new RhinoCompute.Grasshopper.DataTree('RH_IN:201:H_ed');
    param9.append([0], [H_ed]);

    compute();
}

// BOILERPLATE //

var scene, camera, renderer, controls;

//ViewCube Variables
let cubeCameraDistance = 1.75;
let cubeWrapper = document.getElementById('orientCubeWrapper');
let cubeScene = new THREE.Scene();
let cubeCamera = new THREE.PerspectiveCamera(70, cubeWrapper.offsetWidth / cubeWrapper.offsetHeight, 0.1, 100);
let cubeRenderer = new THREE.WebGLRenderer({
    alpha: true,
    antialias: true,
    preserveDrawingBuffer: true
});

function init(){
    scene = new THREE.Scene();
    scene.background = new THREE.Color(1,1,1);
    camera = new THREE.PerspectiveCamera( 45, window.innerWidth/window.innerHeight, 1, 1000 );

    renderer = new THREE.WebGLRenderer({antialias: true});
    renderer.setPixelRatio( window.devicePixelRatio );
    renderer.setSize( window.innerWidth, window.innerHeight );
    var canvas = document.getElementById('canvas');
    canvas.appendChild( renderer.domElement );

    controls = new THREE.OrbitControls( camera, renderer.domElement  );

    camera.position.z = 50;

    window.addEventListener( 'resize', onWindowResize, false );
    viewcube();
    animate();
}

var animate = function () {
    requestAnimationFrame( animate );
    controls.update();
    renderer.render( scene, camera );
    //add viewcube
    updateCubeCamera();
    cubeRenderer.render(cubeScene, cubeCamera);
};
  
function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize( window.innerWidth, window.innerHeight );
    animate();
}

function meshToThreejs(mesh, material) {
    let loader = new THREE.BufferGeometryLoader();
    var geometry = loader.parse(mesh.toThreejsJSON());
    return new THREE.Mesh(geometry, material);
}

// ViewCube
var viewcube = function () {
    cubeRenderer.setSize(cubeWrapper.offsetWidth, cubeWrapper.offsetHeight);
    cubeRenderer.setPixelRatio(window.deivicePixelRatio);

    cubeWrapper.appendChild(cubeRenderer.domElement);

    let materials = [];
    let texts = ['RIGHT', 'LEFT', 'TOP', 'BOTTOM', 'FRONT', 'BACK'];

    let textureLoader = new THREE.TextureLoader();
    let canvas = document.createElement('canvas');
    let ctx = canvas.getContext('2d');

    let size = 64;
    canvas.width = size;
    canvas.height = size;

    ctx.font = 'bolder 12px "Open sans", Arial';
    ctx.textBaseline = 'middle';
    ctx.textAlign = 'center';

    let mainColor = '#fff';
    let otherColor = '#ccc';

    let bg = ctx.createLinearGradient(0, 0, 0, size);
    bg.addColorStop(0, mainColor);
    bg.addColorStop(1, otherColor);

    for (let i = 0; i < 6; i++) {
        if (texts[i] == 'TOP') {
            ctx.fillStyle = mainColor;
        } else if (texts[i] == 'BOTTOM') {
            ctx.fillStyle = otherColor;
        } else {
            ctx.fillStyle = bg;
        }
        ctx.fillRect(0, 0, size, size);
        ctx.strokeStyle = '#aaa';
        ctx.setLineDash([8, 8]);
        ctx.lineWidth = 4;
        ctx.strokeRect(0, 0, size, size);
        ctx.fillStyle = '#999';
        ctx.fillText(texts[i], size / 2, size / 2);
        materials[i] = new THREE.MeshBasicMaterial({
            map: textureLoader.load(canvas.toDataURL())
        });
    }

    let planes = [];

    let planeMaterial = new THREE.MeshBasicMaterial({
        side: THREE.DoubleSide,
        color: 0x00c0ff,
        transparent: true,
        opacity: 0,
        depthTest: false
    });
    let planeSize = 0.7;
    let planeGeometry = new THREE.PlaneGeometry(planeSize, planeSize);

    let a = 0.51;

    let plane1 = new THREE.Mesh(planeGeometry, planeMaterial.clone());
    plane1.position.z = a;
    cubeScene.add(plane1);
    planes.push(plane1);

    let plane2 = new THREE.Mesh(planeGeometry, planeMaterial.clone());
    plane2.position.z = -a;
    cubeScene.add(plane2);
    planes.push(plane2);

    let plane3 = new THREE.Mesh(planeGeometry, planeMaterial.clone());
    plane3.rotation.y = Math.PI / 2;
    plane3.position.x = a;
    cubeScene.add(plane3);
    planes.push(plane3);

    let plane4 = new THREE.Mesh(planeGeometry, planeMaterial.clone());
    plane4.rotation.y = Math.PI / 2;
    plane4.position.x = -a;
    cubeScene.add(plane4);
    planes.push(plane4);

    let plane5 = new THREE.Mesh(planeGeometry, planeMaterial.clone());
    plane5.rotation.x = Math.PI / 2;
    plane5.position.y = a;
    cubeScene.add(plane5);
    planes.push(plane5);

    let plane6 = new THREE.Mesh(planeGeometry, planeMaterial.clone());
    plane6.rotation.x = Math.PI / 2;
    plane6.position.y = -a;
    cubeScene.add(plane6);
    planes.push(plane6);

    let groundMaterial = new THREE.MeshBasicMaterial({
        color: 0xaaaaaa
    });
    let groundGeometry = new THREE.PlaneGeometry(1, 1);
    let groundPlane = new THREE.Mesh(groundGeometry, groundMaterial);
    groundPlane.rotation.x = -Math.PI / 2;
    groundPlane.position.y = -0.6;

    cubeScene.add(groundPlane);

    let cube = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), materials);
    cubeScene.add(cube);

    let activePlane = null;

    cubeRenderer.domElement.onmousemove = function (evt) {

        if (activePlane) {
            activePlane.material.opacity = 0;
            activePlane.material.needsUpdate = true;
            activePlane = null;
        }

        let x = evt.offsetX;
        let y = evt.offsetY;
        let size = cubeRenderer.getSize(new THREE.Vector2());
        let mouse = new THREE.Vector2(x / size.width * 2 - 1, -y / size.height * 2 + 1);

        let raycaster = new THREE.Raycaster();
        raycaster.setFromCamera(mouse, cubeCamera);
        let intersects = raycaster.intersectObjects(planes.concat(cube));

        if (intersects.length > 0 && intersects[0].object != cube) {
            activePlane = intersects[0].object;
            activePlane.material.opacity = 0.2;
            activePlane.material.needsUpdate = true;
        }
    }

    let oldPosition = new THREE.Vector3();
    let newPosition = new THREE.Vector3();

    cubeRenderer.domElement.onclick = function (evt) {

        cubeRenderer.domElement.onmousemove(evt);

        if (!activePlane || hasMoved) {
            return false;
        }

        oldPosition.copy(camera.position);

        let distance = camera.position.clone().sub(controls.target).length();
        newPosition.copy(controls.target);

        if (activePlane.position.x !== 0) {
            newPosition.x += activePlane.position.x < 0 ? -distance : distance;
        } else if (activePlane.position.y !== 0) {
            newPosition.y += activePlane.position.y < 0 ? -distance : distance;
        } else if (activePlane.position.z !== 0) {
            newPosition.z += activePlane.position.z < 0 ? -distance : distance;
        }


        camera.position.copy(newPosition);
    }

    cubeRenderer.domElement.ontouchmove = function (e) {
        let rect = e.target.getBoundingClientRect();
        let x = e.targetTouches[0].pageX - rect.left;
        let y = e.targetTouches[0].pageY - rect.top;
        cubeRenderer.domElement.onmousemove({
            offsetX: x,
            offsetY: y
        });
    }

    cubeRenderer.domElement.ontouchstart = function (e) {
        let rect = e.target.getBoundingClientRect();
        let x = e.targetTouches[0].pageX - rect.left;
        let y = e.targetTouches[0].pageY - rect.top;
        cubeRenderer.domElement.onclick({
            offsetX: x,
            offsetY: y
        });
    }

    let hasMoved = false;

    function antiMoveOnDown(e) {
        hasMoved = false;
    }
    function antiMoveOnMove(e) {
        hasMoved = true;
    }

    window.addEventListener('mousedown', antiMoveOnDown, false);
    window.addEventListener('mousemove', antiMoveOnMove, false);
    window.addEventListener('touchstart', antiMoveOnDown, false);
    window.addEventListener('touchmove', antiMoveOnMove, true);
}

function updateCubeCamera() {
    cubeCamera.rotation.copy(camera.rotation);
    let dir = camera.position.clone().sub(controls.target).normalize();
    cubeCamera.position.copy(dir.multiplyScalar(cubeCameraDistance));
}