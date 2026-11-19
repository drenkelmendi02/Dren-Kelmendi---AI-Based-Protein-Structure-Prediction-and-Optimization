
import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";


function AminoAcid({ position, type, index }) {
    const color = type === "H" ? "red" : "blue";

    return (
        <mesh position={position}>
            <sphereGeometry args={[0.35, 32, 32]} />
            <meshStandardMaterial color={color} />
        </mesh>
    );
}


function ProteinChain({ coordinates, hpSequence }) {
    return (
        <>
            {coordinates.map((point, index) => (
                <AminoAcid
                    key={index}
                    position={[point.x, point.y, point.z]}
                    type={hpSequence[index]}
                    index={index}
                />
            ))}

            {coordinates.slice(0, -1).map((point, index) => {
                const next = coordinates[index + 1];

                const start = [point.x, point.y, point.z];
                const end = [next.x, next.y, next.z];

                const midpoint = [
                    (start[0] + end[0]) / 2,
                    (start[1] + end[1]) / 2,
                    (start[2] + end[2]) / 2
                ];

                const length = Math.sqrt(
                    (end[0] - start[0]) ** 2 +
                    (end[1] - start[1]) ** 2 +
                    (end[2] - start[2]) ** 2
                );

                return (
                    <mesh
                        key={`bond-${index}`}
                        position={midpoint}
                    >
                        <cylinderGeometry args={[0.06, 0.06, length, 12]} />
                        <meshStandardMaterial color="gray" />
                    </mesh>
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
