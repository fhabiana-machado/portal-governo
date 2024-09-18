import React from 'react';
import PropTypes from 'prop-types';
import { Container } from '@plone/components';

const Gestor = (props) => {
  const content = props?.content;
  const { title } = content;
  const img = content.image_scales?.image;
  const scale = img ? img[0]?.scales?.thumb : null;

  return (
    <Container narrow className="gestor-wrapper">
      <h4>Gestor</h4>
      {title && (
        <Container>
          <span className="title">{title}</span>
        </Container>
      )}
      {img ? (
        <img
          src={`${content['@id']}/${scale.download}`}
          alt={`Foto de ${content.title}`}
          className={'portrait listitem'}
        />
      ) : (
        <Icon name={personSVG} size="64px" className={'portrait listitem'} />
      )}
    </Container>
  );
};

export default Gestor;
