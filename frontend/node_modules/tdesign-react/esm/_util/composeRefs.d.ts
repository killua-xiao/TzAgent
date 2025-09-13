import { Ref } from 'react';
export default function composeRefs<T>(...refs: Ref<T>[]): (instance: T) => void;
