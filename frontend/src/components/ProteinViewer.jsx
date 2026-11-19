
import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import { Vector3, Quaternion } from "three";


function AminoAcid({ position, type }) {
    const color = type === "H" ? "red" : "blue";

    return (
        <mesh position={position}>
            <sphereGeometry args={[0.35, 32, 32]} />
            <meshStandardMaterial color={color} />
        </mesh>
    );
}


function Bond({ start, end }) {
    const startVector = new Vector3(...start);
    const endVector = new Vector3(...end);

    const direction = new Vector3()
        .subVectors(endVector, startVector);

    const length = direction.length();

    const midpoint = new Vector3()
        .addVectors(startVector, endVector)
        .multiplyScalar(0.5);

    const quaternion = new Quaternion()
        .setFromUnitVectors(
            new Vector3(0, 1, 0),
            direction.normalize()
        );

    return (
        <mesh
            position={midpoint.toArray()}
            quaternion={quaternion}
        >
            <cylinderGeometry args={[0.06, 0.06, length, 12]} />
            <meshStandardMaterial color="gray" />
        </mesh>
    );
}


function ProteinChain({ coordinates, hpSequence }) {
    return (
        <>
            {coordinates.map((point, index) => (
                <AminoAcid
                    key={`amino-${index}`}
                    position={[point.x, point.y, point.z]}
                    type={hpSequence[index]}
                />
            ))}

            {coordinates.slice(0, -1).map((point, index) => {
                const next = coordinates[index + 1];

                return (
                    <Bond
                        key={`bond-${index}`}
                        start={[point.x, point.y, point.z]}
                        end={[next.x, next.y, next.z]}
                    />
                );
            })}
        </>
    );
}


export default function ProteinViewer({
    coordinates = [],
    hpSequence = ""
}) {
    return (
        <div style={{ width: "100%", height: "500px" }}>
            <Canvas camera={{ position: [8, 8, 10], fov: 50 }}>
                <ambientLight intensity={0.8} />

                <directionalLight
                    position={[5, 5, 5]}
                    intensity={1.5}
                />

                <ProteinChain
                    coordinates={coordinates}
                    hpSequence={hpSequence}
                />

                <OrbitControls makeDefault />
                <gridHelper args={[20, 20]} />
                <axesHelper args={[5]} />
            </Canvas>
        </div>
    );
}
