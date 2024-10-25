import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { withBlockExtensions } from '@plone/volto/helpers';
import { listSecretarias } from '../../../actions/secretarias/secretarias';
import SecretariasView from './DefaultView';
const SecretariasBlockView = (props) => {
  const { data, isEditMode, className } = props;
  const dispatch = useDispatch();
  const secretarias = useSelector((state) => state.secretarias?.data);
  // Dispara chamada na criação da constante dispatch
  useEffect(() => {
    dispatch(listSecretarias());
  }, [dispatch]);

  return (
    <SecretariasView
      {...data}
      secretarias={secretarias}
      isEditMode={isEditMode}
      className={className}
    />
  );
};
export default withBlockExtensions(SecretariasBlockView);
