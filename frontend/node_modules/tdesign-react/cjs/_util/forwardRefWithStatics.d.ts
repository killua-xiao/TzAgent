import React, { RefAttributes } from 'react';
export default function forwardRefWithStatics<P, T = any, S = {}>(component: React.ForwardRefRenderFunction<T, P>, statics?: S): React.FunctionComponent<P & RefAttributes<T>> & S;
