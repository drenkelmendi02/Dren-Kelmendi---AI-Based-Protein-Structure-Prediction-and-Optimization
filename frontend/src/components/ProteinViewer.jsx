
import {
    Canvas
} from "@react-three/fiber";

import {
    OrbitControls,
    Bounds,
    Center
} from "@react-three/drei";

import {
    Vector3,
    Quaternion
} from "three";


/* =========================================
   AMINO ACID
========================================= */

function AminoAcid({ position, type, index }) {

    const color = type === "H" ? "#ef4444" : "#38bdf8";

    return (
        <mesh position={position}>
            <sphereGeometry args={[0.22, 24, 24]} />

            <meshStandardMaterial
                color={color}
                roughness={0.35}
                metalness={0.15}
            />
        </mesh>
    );
}


/* =========================================
   BOND BETWEEN AMINO ACIDS
========================================= */

function Bond({ start, end }) {

    const startVector = new Vector3(...start);
    const endVector = new Vector3(...end);

    const direction = new Vector3().subVectors(
        endVector,
        startVector
    );

    const length = direction.length();

    const midpoint = new Vector3()
        .addVectors(startVector, endVector)
        .multiplyScalar(0.5);

    const quaternion = new Quaternion();

    quaternion.setFromUnitVectors(
        new Vector3(0, 1, 0),
        direction.clone().normalize()
    );

    return (
        <mesh
            position={midpoint.toArray()}
            quaternion={quaternion}
        >
            <cylinderGeometry
                args={[0.055, 0.055, length, 12]}
            />

            <meshStandardMaterial
                color="#94a3b8"
                roughness={0.5}
            />
        </mesh>
    );
}


/* =========================================
   PROTEIN CHAIN
========================================= */

function ProteinChain({ coordinates, hpSequence }) {

    const positions = coordinates.map((coordinate) => [
        coordinate.x,
        coordinate.y,
        coordinate.z
    ]);

    return (
        <group>

            {/* Bonds */}
            {positions.slice(0, -1).map((position, index) => (
                <Bond
                    key={`bond-${index}`}
                    start={position}
                    end={positions[index + 1]}
                />
            ))}


            {/* Amino acids */}
            {positions.map((position, index) => (
                <AminoAcid
                    key={`amino-${index}`}
                    position={position}
                    type={hpSequence[index]}
                    index={index}
                />
            ))}

        </group>
    );
}


/* =========================================
   MAIN 3D VIEWER
========================================= */

function ProteinViewer({
    coordinates = [],
    hpSequence = ""
}) {

    if (!coordinates.length) {
        return (
            <div className="protein-viewer-container">
                <p>No protein coordinates available.</p>
            </div>
        );
    }

    return (
        <Canvas
            camera={{
                position: [8, 8, 8],
                fov: 50
            }}
        >

            {/* Lighting */}
            <ambientLight intensity={0.8} />

            <directionalLight
                position={[10, 10, 10]}
                intensity={1.5}
            />

            <pointLight
                position={[-10, -10, -10]}
                intensity={0.5}
            />


            {/* Protein visualization */}
            <Bounds
                fit
                clip
                observe
                margin={1.5}
            >
                <Center>
                    <ProteinChain
                        coordinates={coordinates}
                        hpSequence={hpSequence}
                    />
                </Center>
            </Bounds>


            {/* Reference grid */}
            <gridHelper
                args={[20, 20, "#334155", "#1e293b"]}
            />

            <axesHelper args={[3]} />


            {/* Mouse controls */}
            <OrbitControls
                makeDefault
                enableDamping
                dampingFactor={0.08}
                minDistance={2}
                maxDistance={100}
            />

        </Canvas>
    );
}

export default ProteinViewer;
